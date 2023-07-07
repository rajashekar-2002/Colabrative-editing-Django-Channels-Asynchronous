from django.shortcuts import render,redirect
from .models import Group
from signin.models import User
from django.db.models import Q
from .models import Collabnote
# Create your views here.
def collabrate(request):
    email=request.session.get('user')
    grps=Group.objects.all().filter(user__email=email)
    return render(request,'collabrate.html',{'grps':grps})


def addgrp(request):
    if request.method=='POST':
        grpname=request.POST.get('grpname')
        desc=request.POST.get('desc')
        request.session['desc']=desc
        email=request.session.get('user')
        grp=Group.objects.filter(grpname=grpname).first()
        if grp:
            pass
        else:
            user=User.user_object(email)
            grp=Group(grpname=grpname,description=desc,createdby=email,user=user)
            grp.save()
        return redirect('collabrate')
        

            
        
def selectgrp(request,grpname):
    request.session['grpname']=grpname
    
    email=request.session.get('user')
    grpname=request.session.get('grpname')
    group=Group.getgrpobj(email,grpname)
    request.session['createdby']=group.createdby
    request.session['grpdate']=str(group.date)
    try:
        participants=group.participants
        participants_list=participants.split()
    except:
        participants_list=None
    return render(request,'colabnote.html',{'participants':participants_list})




def addpart(request):
    if request.method=='POST':
        part_email=request.POST.get('email')
        email=request.session.get('user')
        grpname=request.session.get('grpname')
        group=Group.getgrpobj(email,grpname)
        print(group)
        if group.participants is not None:
            participants=group.participants
            participants_list=participants.split()
        else:
            group.participants = email
            group.save()
            participants_list=group.participants.split()
        if part_email in participants_list:
            pass
        else:
            object=User.user_object(part_email)
            if object:
                group.participants=participants+' '+part_email
                group.save()
                desc=request.session.get('desc')
                
                newgroup=Group(grpname=grpname,description=desc,createdby=email,participants=participants,user=object)
                newgroup.save()


                participants_list=participants.split()
    return render(request,'colabnote.html',{'participants':participants_list})
        



def savenote(request):
    email=request.session.get('user')
    grpname=request.session.get('grpname')
    textarea=request.POST.get('mytextarea')
    group=Group.getgrpobj(email,grpname)
    note=Collabnote.objects.filter(Q(name=grpname) & Q(user__email=email)).first()
    if note:
        note.content=textarea
        note.save()
    else:
        user=User.user_object(email)
        chat=Collabnote(name=grpname,content=textarea,group=group,user=user)
        chat.save()

    grpname=request.session.get('grpname')
    group=Group.getgrpobj(email,grpname)
    
    participants=group.participants
    participants_list=participants.split()

    return render(request,'colabnote.html',{'participants':participants_list,'content':textarea})