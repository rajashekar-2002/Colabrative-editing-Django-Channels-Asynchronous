from django.shortcuts import render,redirect
from django.http import HttpResponse
from notes.models import Notes
from notebook.models import Notebook
from signin.models import User
# from notebook.views import signin_required
from django.db.models import Q
from notes.models import Attachment
from django.utils.text import slugify
from django.utils import timezone
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

                if abs(now-last) > timedelta(minutes=10):
                    return redirect('signin')
            except:
                request.session['last_activity']=str(now)



        return function(request, *args, **kwargs)
    return inner
    




@signin_required
def notes_by_notebook(request,slug):
    email=request.session.get('user')
    # slug=request.GET.get('slug') 
    notes=Notes.get_notes_by_name(slug,email)
    print(slug)
    count=Notebook.objects.get(Q(notebook_slug=slug) & Q(user__email=email)).notes.count()
    print(count)
    request.session['notebook']=slug
    return render(request,'notes.html',{'notes':notes,'count':count,'slug':slug})


@signin_required
def selectnotes(request,notebook,note):
    email=request.session.get('user')
    print(';;;;;;;;;;;;;;;;;;;;;;;',email)
    content=Notes.get_content_by_notes(note,email)
    print(';;;;;;;;;;;;;;',content.notes_text)
    notes=Notes.get_notes_by_name(notebook,email)
    request.session['note']=note
    #add after tags
    object=Notes.get_notes_from_book_note(notebook,note,email)
    text=object.tags
    text=text.split()
    request.session['session_tag']=text
    file=Attachment.objects.all().filter(notes__notes_slug=note)
    print(file)


    all_notebook=Notebook.user_notebook(email)
    all_notes=Notes.user_notes(email)
    return render(request,'notes.html',{'notes_content':content,'notes':notes,'slug':notebook,'file':file,'all_notebook':all_notebook,'all_notes':all_notes})

@signin_required
def notes_search(request,**kwargs):
    slug=request.session.get('notebook')
    email=request.session.get('user')
    notes=Notes.get_notes_by_name(slug,email)
    
    if(request.method=='POST'):
        count=Notebook.objects.get(Q(notebook_slug=slug) & Q(user__email=email)).notes.count()
        query=request.POST.get('notes_search')
        if query:
            items=Notes.objects.filter(Q(notes_name__icontains=query) & Q(notebook__user__email=email) | Q(tags__icontains=query))
        else:
            items=[]
        context={'items':items,'query':query,'notes':notes,'count':count,'slug':slug}
        return render(request,'notes.html',context)
    
    # if(request.method=='GET'):
    #     # from search all tabs with kwargs as parameters
    #     book_name=kwargs['notebook_slug']
    #     note=kwargs['note']
    #     notes=Notes.objects.filter(Q(notes_name=note) & Q(notebook__user__email=email) | Q(notebook__book_name=book_name))
    #     context={'items':items,'query':query,'notes':notes,'count':count,'slug':book_name}
    #     return render(request,'notes.html',context)



@signin_required
def tags(request):
    if(request.method=='POST'):
        email=request.session.get('user')
        tag=request.POST.get('tags')
        notebook=request.session.get('notebook')
        note=request.session.get('note')
        print('[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]')
        print(email)
        print(tag)
        print(notebook)
        print(note)
        object=Notes.get_notes_from_book_note(notebook,note,email)
        # object=Notes.objects.all().filter(Q(notebook__notebook_slug=notebook) & Q(notes_slug=note) & Q(notebook__user__email=email)).first()
        print(object)
        print(object.tags)
        text=object.tags
        object.tags=text+' '+ tag +' '
        object.save()
        # text=object.tags
        text=text.split()
        request.session['session_tag']=text
        # session_tag=request.session.get('session_tag')
        # if session_tag:
        #     session_tag['note'] +=[tags]
        # else:
        #     session_tag={}
        #     session_tag['note']=[tags]
        #     request.session['session_tag']=session_tag

        redirect_to_note='/notes/'+ notebook +'/content/' + note 
        # /notes/first-book/content/vjvh
        return redirect(redirect_to_note)

@signin_required
def delete_tag(request):
    email=request.session.get('user')
    if request.method=='GET':
        delete_tag=request.GET.get('delete_tag')
        print('tag',delete_tag)
        notebook=request.session.get('notebook')
        note=request.session.get('note')
        object=Notes.get_notes_from_book_note(notebook,note,email)
        text=object.tags
        words=text.split()
        print('words',words)
        flag=False

        for word in words:
            print('word',word)
            if word==delete_tag:
                words.remove(word)
                print('remove',words)
                flag=True
                print('word',word)

        if flag==True:
            request.session['session_tag']=words
            text=' '.join(words)
        print('text',text)
        object.tags=text
        object.save()
        redirect_to_note='/notes/'+ notebook +'/content/' + note 
        # /notes/first-book/content/vjvh
        return redirect(redirect_to_note)
        

@signin_required
def content(request):
    if request.method=='POST':
        content=request.POST.get('mytextarea')
        email=request.session.get('user')
        notebook=request.session.get('notebook')
        note=request.session.get('note')
        print(content)
        Notes.save_content(notebook,note,email,content)
        
        # not creating object but updating
        # object.update(notes_text=content)
        redirect_to_note='/notes/'+ notebook +'/content/' + note 
        # /notes/first-book/content/vjvh
        return redirect(redirect_to_note)

@signin_required
def bookmark_notes(request,slug,bookmark):
    if request.method=='GET':
    
        email=request.session.get('user')
        print(bookmark)
        object=Notes.objects.filter(Q(notebook__user__email=email) & Q(notebook__book_name=slug) & Q(notes_name=bookmark)).first()
        print(',,,,,,,,,,,,,,,,,,,,,,,,,',object)
        if object.bookmark_notes == True:
            Notes.objects.filter(Q(notebook__book_name=slug) & Q(notebook__user__email=email) & Q(notes_name=bookmark)).update(bookmark_notes=False)
        else:
            Notes.objects.filter(Q(notebook__book_name=slug) & Q(notebook__user__email=email) & Q(notes_name=bookmark)).update(bookmark_notes=True)
        return redirect(request.META['HTTP_REFERER'])




def attachment(request):
    if request.method=='POST':
        print('//////////////////////////////////')
        email=request.session.get('user')
        notebook=request.POST.get('notebook')
        note=request.POST.get('note')
        file=request.FILES['attachment']
        print('//...........................',file.size)
        print(email,notebook,note)
        # object=Notes.objects.filter(Q(notebook__user__email=email) & Q(notebook__notebook_slug=notebook) & Q(notes_name=note)).update(attach=file)
        # object=Notes.get_notes_from_book_note(notebook,note)
        print(object)
        note_object=Notes.get_content_by_notes(note,email)
        print('///////////////////////',note)
        print(note_object.notes_text)
        # user=User.user_object(email)
        attach=Attachment.objects.create(attach=file,notes=note_object)
        attach.save()
        
            # object(attach=i).save()
            # object.attach.save( file, save=True)
        # instance = object(attach=request.FILES['attachment'])
        # instance.save()

        print('file uploaded....................')
    return redirect(request.META['HTTP_REFERER'])



def delete_img(request):
    if request.method=='GET':
        delete_img=request.GET.get('delete_img')
        note=request.session.get('note')
        Attachment.objects.filter(Q(notes__notes_slug=note) & Q(attach=delete_img)).first().delete()
        return redirect(request.META['HTTP_REFERER'])



@signin_required
def new_notes(request):
    if request.method=='POST':
        email=request.session.get('user')
        notebook=request.session.get('notebook')
        note_name=request.POST.get('note_name')
        notebook_obj=Notebook.get_notebook(notebook,email)
        note_obj=Notes(notes_name=note_name,notebook=notebook_obj,notes_slug=slugify(note_name))
        note_obj.save()
    return redirect(request.META['HTTP_REFERER'])




@signin_required
def sort(request):
    if request.method=='GET':
        email=request.session.get('user')
        sort=request.GET.get('sort')
        if sort=='A-Z':
            notes=Notes.objects.all().filter(notebook__user__email=email).order_by('notes_name')
        if sort=='Z-A':
            notes=Notes.objects.all().filter(notebook__user__email=email).order_by('-notes_name')
        if sort=='bookmark':
            notes=Notes.objects.all().filter(Q(notebook__user__email=email) & Q(bookmark_notes='True'))
        if sort=='recent_used':
            notes=Notes.objects.all().filter(notebook__user__email=email).order_by('-notes_last_modified')
        if sort=='created_on':
            notes=Notes.objects.all().filter(notebook__user__email=email).order_by('-notes_created_on')
    # return to notes_by notebook
    slug=request.session['notebook']
    count=Notebook.objects.get(Q(notebook_slug=slug) & Q(user__email=email)).notes.count()
    return render(request,'notes.html',{'notes':notes,'count':count,'slug':slug})

