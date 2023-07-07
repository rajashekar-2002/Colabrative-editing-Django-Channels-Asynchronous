from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
scheduler = BackgroundScheduler()
from datetime import datetime, timedelta
# from dateutil.parser import parse
from datetime import datetime, timedelta
from django.shortcuts import redirect


# pip install django-apscheduler
def pop_message(request,task_name,task_date):
    
    request.session['task_name']=str(task_name)
    print(task_name)
    # task['task_name']=task_name
    print(task_date)
    request.session['task_date']=str(task_date)
    
    # request.session.save()
    print(request.session.get('task_name'))
    # session = SessionStore()
    request.session.save()
    # session_engine = settings.SESSION_ENGINE
    print('bkjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjhere')
    # return redirect('task')


    
def schedule_task(request,task_name, ring_time,task_date):
    # session = SessionStore()
    # session['raju']='raju'
    # session.save()
    request.session['raju']='gggggggggggggggggggggggggg'
    
    ring_time=abs(ring_time)
    print('schleduled time on ..............................////',ring_time)
    # duration_str = str(ring_time)
    # try:
    #     duration = parse(duration_str)
    #     timedelta_duration = timedelta(days=duration.day, hours=duration.hour, minutes=duration.minute, seconds=duration.second, microseconds=duration.microsecond)
    #     print('///////////////////////////herereererere')
    # except:
    #     # timedelta_duration = timedelta( seconds=duration.second, hours=duration.hour, minutes=duration.minute, microseconds=duration.microsecond)
    #     print('vjhvvvvvvvvvvvvvvvvvvvvvv')
    #     time_str=duration_str
    #     days_str, time_str = time_str.split(", ")
    #     days = int(days_str.split()[0])
    #     hours, minutes, seconds = map(float, time_str.split(":"))
    #     # Convert to total seconds
    #     total_seconds = days * 24 * 3600 + hours * 3600 + minutes * 60 + seconds
    #     # Create a timedelta object representing the time interval
    #     timedelta_duration = timedelta(seconds=total_seconds)
    #     # Format the timedelta object as "h m s.p"
    #     # hours, remainder = divmod(delta.total_seconds(), 3600)
    #     # minutes, seconds = divmod(remainder, 60)
    #     # milliseconds = int(delta.microseconds / 1000)
    #     # timedelta_duration = f"{int(hours):d}h {int(minutes):d}m {int(seconds):d}.{milliseconds:03d}s"
    # now = datetime.now()
    # result_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
    # end_time = result_time + ring_time
    # endtime=endtime.strftime("%H:%M:%S")
    request.session['time']=str(ring_time)
    # request.session['end_time']=str(end_time)
    request.session['time_now']=str(datetime.now()+ring_time)

    scheduler = BackgroundScheduler()
    # scheduler.configure(misfire_grace_time=30*60)
    # scheduler.remove_all_jobs()
    # scheduler.add_job(pop_message, 'date', args=[request,task_name,task_date], run_date=end_time)
    # scheduler.add_job(my_job, 'date', run_date='2023-05-01 12:00:00')
    # scheduler.add_job(pop_message, 'date', run_date='2023-04-30 00:00:15')
    scheduler.add_job(pop_message, trigger='date', args=[request,task_name,task_date], run_date=datetime.now() + ring_time)
    scheduler.start()
    # scheduler.shutdown()
    # if not written error after reloading page



    # return redirect(request.META['HTTP_REFERER'])



    # delta_str = "2 days, 2:08:51.696548"  # Example duration string
    # delta = timedelta(days=int(ring_time.split()[0]), hours=int(ring_time.split()[2].split(':')[0]), minutes=int(ring_time.split()[2].split(':')[1]), seconds=float(ring_time.split()[2].split(':')[2]))
    # run_time = datetime.now() + delta