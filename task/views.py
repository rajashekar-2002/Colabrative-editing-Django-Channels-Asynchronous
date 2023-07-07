from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Task
from signin.models import User
from django.db.models import F
from datetime import datetime
from .managements import schedule_task
from django.contrib.sessions.backends.db import SessionStore
from django.contrib import messages #import messages
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
# from .management.commands.sch_task import pop
# Create your views here.
from django.contrib.sessions.backends.db import SessionStore
global cnt
from datetime import datetime, timedelta

from django.utils import timezone


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
                if abs(now-last) > timedelta(seconds=960):
                    # request.session['last_activity']=str(now)
                    return redirect('signin')
            except:
                request.session['last_activity']=str(now)

        
        return function(request, *args, **kwargs)
    return inner
    
# uses toat 

@signin_required
def task(request):
    if request.method=='GET':
        email=request.session.get('user')
        due_task=Task.get_due_task(email)
        overdue_task=Task.get_overdue_task(email)
        
        # scheduler = BackgroundScheduler()
        # # request.session['job']=None
        # def pop(request):
        #     print('bkjjjjjjjjjhere')
        #     request.session['task']='hhhhhhhhhhhhhhhhh'
        #     request.session['job']='done'
        #     request.session.save()
        #     # session = SessionStore()
        #     # session.save()
            
        #     try:
        #         print('in')
        #         print(request.session.get('job'))
        #     except:
        #         print('out')

        # #     return redirect(request.META['HTTP_REFERER'])
            
            
            
    
        # scheduler.add_job(pop, trigger='interval',args=[request], seconds=15)
        # scheduler.add_job(pop, trigger='date', args=[request], run_date=datetime.now() + timedelta(seconds=15))
        # scheduler.start()

     
        request.session['task_name']='None'
        if due_task:
            request.session['inif']='inif'
            schedule_task(request,due_task[0].task_name, due_task[0].time_diff,due_task[0].task_date)
        count=Task.count_user_task(email)
        return render(request,'task.html',{'count':count,'due_task':due_task,'overdue':overdue_task})

@signin_required
def add_task(request):
    if request.method=='POST':
        email=request.session.get('user')
        task=request.POST.get('task')
        datetime=request.POST.get('datetime')
        user=User.user_object(email)
        object=Task(task_name=task,task_date=datetime,user=user)
        object.save()
        return redirect('task')

@signin_required
def delete_overdue_task(request):
    if request.method=='GET':
        email=request.session.get('user')
        Task.get_overdue_task_delete(email)
        return redirect('task')

@signin_required
def delete_task(request,task_name):
    if request.method=='GET':
        email=request.session.get('user')
        Task.task_delete_by_name(email,task_name)
        return redirect('task')

