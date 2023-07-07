from django.shortcuts import render,redirect
from notes.models import Notes
from task.models import Task
from notebook.models import Notebook
from datetime import datetime
from django.utils.text import slugify
from signin.models import User
from django.db.models import Q
from .models import Shared_with_me
from notes.models import Attachment
# Create your views here.
from django.utils import timezone
import pytz
tz = pytz.timezone('Asia/Kolkata')
from datetime import datetime, timedelta



def signin_required(function):
    def inner(request, *args, **kwargs):
        email=request.session.get('user')
        now = datetime.now()
        now=now.replace(microsecond=0)
        
        if email==None:
            return redirect('signup')
        else:
            try:
                
                last=request.session.get('last_activity')
                last = datetime.strptime(last, "%Y-%m-%d %H:%M:%S")
                # last=datetime(2023, 5, 16, 15, 9, 28)

                print(type(last))
                print(last)
                request.session['last_activity']=str(now)
                if abs(now-last) > timedelta(seconds=15000):
                    # request.session['last_activity']=str(now)
                    return redirect('signin')
            except:
                request.session['last_activity']=str(now)

        
        return function(request, *args, **kwargs)
    return inner
    



# Create your views here.
@signin_required
def home(request):
    email=request.session.get('user')
    all_notebook=Notebook.user_notebook(email)
    all_notes=Notes.user_notes(email)
    notes=Notes.recent_updated_notes(email)
    task=Task.get_all__user_task(email)
    if request.method=='GET':
        


        
        print(email)
        # variable=request.GET.get('variable')
        
        
        variable=Notes.user_notes(email)

   

    
        return render(request,'home.html',{'notes':notes,'task':task,'variable':variable,'all_notebook':all_notebook,'all_notes':all_notes})
 
        
    else:

        if request.POST['submit_button'] == 'allnotes':
            variable=Notes.user_notes(email)
        if request.POST['submit_button'] == 'favourites':
            variable=Notes.objects.all().filter(Q(notebook__user__email=email) & Q(bookmark_notes=True))
                    # return render(request,'attachments.html',{'notes':notes,'task':task,'attach':variable})

                # if variable=='allnotes':
                #     all_notes=Notes.user_notes(email)
                # else:
                #     all_notes=Notes.objects.filter(Q(user__email=email) & Q(bookmark_notebook=True))
                # notes=Notes.user_notes_recent_updated(email)

                # all_notes=Notes.get_all_notes()
                # task=Task.get_all_task()

        return render(request,'home.html',{'notes':notes,'task':task,'variable':variable})


# @signi    n_required
# def home_tabs(request,variable):
#     if variable=='allnotes':
#         return redirect('notebook',variable)
#     else:
#         return


@signin_required
def notebook(request):
    email=request.session.get('user')
    if(request.method=='GET'):
        # request.session['last_activity'] = 'nowvjhvj'
        
        # notebook=Notebook.get_all_notebook()
        # count=Notebook.objects.all().count()
        all_notebook=Notebook.user_notebook(email)
        all_notes=Notes.user_notes(email)
        # for all search
        email=request.session.get('user')
        notebook=Notebook.user_notebook(email)
        count=Notebook.user_notebook_count(email)
        return render(request,'notebook.html',{'notebook':notebook,'count':count,'all_notebook':all_notebook,'all_notes':all_notes})
    else:
        # notebook search
        # notebook=Notebook.get_all_notebook()
        # count=Notebook.objects.all().count()
        # email=request.session.get('user')
        notebook=Notebook.user_notebook(email)
        count=Notebook.user_notebook_count(email)
        query=request.POST.get('notebook_search')
        
        if query:
            # items=Notebook.objects.filter(book_name__icontains=query)
            items=Notebook.objects.filter(Q(user__email=email) & Q(book_name__icontains=query))
        else:
            items=[]
        context={'items':items,'query':query,'notebook':notebook,'count':count}
    
        return render(request,'notebook.html',context)


@signin_required
def new_notebook(request):
    email=request.session.get('user')
    notebook=Notebook.user_notebook(email)
    count=Notebook.user_notebook_count(email)
    if(request.method=='POST'):

        name=request.POST.get('notebook_name')
        user=User.user_object(email)
        # user=User.objects.create(email='ugbbjh@gmail.com',password='12')
        
        


        print('ooooooooooooooooooooo',user)
        slug=slugify(name)
        # bool="False"
        check=Notebook.check_notebook(name,email)
        print(check)
        if check is not True:
            notebook_obj=Notebook(book_name=name,notebook_slug=slug,bookmark_notebook=False,user=user)
            notebook_obj.save()
            success='Notebook successfully created..'
            return render(request,'notebook.html',{'notebook':notebook,'count':count,'success':success})
        else:
            error='Notebook already exist..'
            return render(request,'notebook.html',{'error':error,'notebook':notebook,'count':count})
    else:
        return render(request,'notebook.html',{'notebook':notebook,'count':count,'check':check})




@signin_required
def share_notebook(request):
    user_email=request.session.get('user')
    if request.method=='POST':
        email=request.POST.get('email')
        notebook=request.POST.get('notebook')
        notebook_slug=slugify(notebook)
        
        notebook_object=Notebook.get_notebook(notebook,user_email)
        # check if user already have same notebook
        user_object=Notebook.check_user_and_notebook_exist(notebook,email)
        print('-----------------',user_object)
        share_error=None
        if user_object:
            notebook_object=Notebook(book_name=notebook_object.book_name,notebook_slug=notebook_slug,bookmark_notebook=False,user=user_object)
            notebook_object.save()
            notes=Notes.get_notes_by_book_name(notebook,user_email)
            for i in notes:
                notes_object=Notes(notes_name=i.notes_name,notes_text=i.notes_text,tags=i.tags,notebook=notebook_object,notes_slug=i.notes_slug)
                
                
                notes_object.save()
                print('bbbbbbbbbbbbbbb',notebook_object)

                # attach_obj=Attachment.return_notes_attach(i.notes_name,user_email)
                try:
                    attach_obj=Attachment.objects.all().get(Q(notes__notes_name=i.notes_name) & Q(notes__notebook__user__email=user_email))
                
                    print('00000000000000',attach_obj)
                    attach_new_obj=Attachment.objects.create(notes=notes_object)
                
                    with attach_obj.attach.open() as f:
                        attach_new_obj.attach.save(attach_obj.attach.name,f)
                    attach_new_obj.save()
                except:
                    pass
                
                
            Shared_with_me.update_shared_with_me(notebook_object.book_name,email,user_object,user_email,notebook_slug)
            return redirect('notebook')
        else:    
            share_error='notebook cannot be shared...'
            # return render(request,'notebook.html',{'error':error})
            notebook=Notebook.user_notebook(user_email)
            count=Notebook.user_notebook_count(user_email)
            return render(request,'notebook.html',{'notebook':notebook,'count':count,'share_error':share_error})


@signin_required
def share_with_me_notebook(request):
    if request.method=='GET':
        email=request.session.get('user')
        print(email)
        object=Shared_with_me.return_shared_notebook(email)
        print(object)
        return render(request,'share_with_me.html',{'object':object})


@signin_required
def bookmark(request,bookmark):
    book_name=bookmark
    email=request.session.get('user')
    object=Notebook.objects.filter(Q(user__email=email) & Q(book_name=book_name)).first()
    if object.bookmark_notebook == True:
        Notebook.objects.filter(Q(user__email=email) & Q(book_name=book_name)).update(bookmark_notebook=False)
    else:
        Notebook.objects.filter(Q(user__email=email) & Q(book_name=book_name)).update(bookmark_notebook=True)
    return redirect('notebook')



@signin_required
def sort(request,sort):
    email=request.session.get('user')
    count=Notebook.user_notebook_count(email)
    if sort=='A-Z':
        notebook=Notebook.objects.all().filter(user__email=email).order_by('book_name')
    if sort=='Z-A':
        notebook=Notebook.objects.all().filter(user__email=email).order_by('-book_name')
    if sort=='bookmark':
        notebook=Notebook.objects.all().filter(Q(user__email=email) & Q(bookmark_notebook='True'))
    if sort=='recent_used':
        notebook=Notebook.objects.all().filter(user__email=email).order_by('-book_last_modified')
    if sort=='created_on':
        notebook=Notebook.objects.all().filter(user__email=email).order_by('-book_created_on')
    return render(request,'notebook.html',{'notebook':notebook,'count':count})
    



@signin_required
def showtags(request):
    email=request.session.get('user')
    if request.method=='GET':
        object=Notes.get_all_user_tags(email)
        # object.exclude(tags__contains='none')
        count=0
        for i in object:
            print(i.tags)
            text=i.tags.split()
            print(text)
            for i in text:
                if i !='none':
                    count=count+1
        return render(request,'tags.html',{'notes':object,'count':count})
    else:
        tags=request.POST.get('tags')
        try:
            object=Notes.objects.filter(Q(notebook__user__email=email) & Q(tags__icontains=tags))
            count=0
            for i in object:
                print(i.tags)
                text=i.tags.split()
                print(text)
                for i in text:
                    if i !='none':
                        count=count+1
        except:
            pass
        return render(request,'tags.html',{'notes':object,'count':count})


    
@signin_required
def searchall(request):
    if request.method=='POST':
        # email=request.session.get('user')
        search=request.POST.get('search')


        
        if search[0] == '#':
            print(search)
            words = search.split(" / ")
            # words = words.replace("#", "")  not work becaz it is list
            tag=words[0].replace("#", "")  
            note=words[1].replace(" ", "") 
            notebook=words[2].replace(" ", "") 
            print(tag,note,notebook)
            print(search)
            request.session['note']=slugify(note)
            request.session['notebook']=slugify(notebook)
            return redirect('/notes/{}/content/{}'.format(notebook,note))





        elif '/' in search:
            print(search)
            note = search.split(" /")[0]
            # note=note.replace(" ", "")
            notebook = search.split("/ ")[1]
            request.session['note']=slugify(note)
            request.session['notebook']=slugify(notebook)
            # notebook=notebook.replace(" ", "")
            print(note,notebook)
            return redirect('/notes/{}/content/{}'.format(notebook,note))
        

        else:
            print(search)

            request.session['notebook']=slugify(search)
            return redirect('/notes/{}'.format(slugify(search)))

            


        