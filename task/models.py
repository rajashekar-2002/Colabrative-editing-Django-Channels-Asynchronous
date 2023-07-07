from django.db import models
from signin.models import User
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from datetime import datetime
# from django.db.models import F
import time
import pytz
tz = pytz.timezone('Asia/Kolkata')


# Create your models here.
class Task(models.Model):
    task_name=models.CharField(max_length=20,null=False,blank=False)
    task_date = models.DateTimeField()
    time_diff=models.DurationField(null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=None)

    class Meta:
        unique_together=[['task_name','user']]

    # def save(self, *args, **kwargs):
    #     if self.task_date:
    #         now=datetime.now()
    #         # timezone = pytz.timezone('UTC')
    #         # aware_datetime = timezone.localize(now)
    #         date_object = datetime.strptime(self.task_date, '%Y-%m-%dT%H:%M')
    #         time_diff = now - date_object
    #         self.time_diff= time_diff
    #     super().save(*args, **kwargs)

    #to upadte task ring time all time make a function and call when task is called by get


    # def save(self, *args, **kwargs):
    #     if self.task_date:
    #         Task.objects.annotate( diff=datetime.now() - F('task_date'))
    #     super(Task, self).save(*args, **kwargs)

    # @property
    # def diff(self):
    #     return datetime.now() - self.task_date
        
    # def save(self, *args, **kwargs):
    #     if self.task_date:
    #         t=datetime.now()
    #         t=t.strftime('%Y-%m-%d %H:%M:%S')
    #         d=self.task_date
    #         self.time_diff = t-d
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.task_name

    @staticmethod
    def get_all_task():
        return Task.objects.all()

    @staticmethod
    def get_all__user_task(email):
        return Task.objects.all().filter(user__email=email).order_by('task_date')[:5]

    @staticmethod
    def get_due_task(email):
        objects=Task.objects.all().filter(user__email=email)
        for i in objects:
            # if i.task_date.date()==time.strftime("%Y-%m-%d"):
            #     time_diff=i.task_date-datetime.now(tz).time()
            #     Task.objects.filter(task_name=i.task_name).update(time_diff=time_diff)

            # now=i.task_date

            # print('now',now.strftime("%z"))
            # date_string = now.strftime('%Y-%m-%dT%H:%M')
            # #task_date=str(i.task_date)
            # date_object = datetime.strptime(date_string , '%Y-%m-%dT%H:%M')

            # kolkata_tz = pytz.timezone('Asia/Kolkata')
            # dt_kolkata = kolkata_tz.localize(date_object)
            # print(dt_kolkata.strftime("%z"))
       
            time_diff =i.task_date- datetime.now(tz) 

            print(time_diff)
            # try:
            #     time_str = str(time_diff)
            #     print('sbdajkjdbkajbkjdkjbkjbkjsbjbk',time_str)
            #     # Parse the time string as a datetime object
            #     dt = datetime.strptime(time_str, '%H:%M:%S.%p')
            #     # Format the datetime as a string in "hh:mm:ss" format
            #     time_str_formatted = dt.strftime('%H:%M:%S')
            #     print('llllllllllllllllllllllll',time_str_formatted)  # Output: 06:30:45

            # except:
            #     duration_str = str(time_diff)
            #     # Split the duration string into its components
            #     duration_parts = duration_str.split(', ')
            #     days = int(duration_parts[0].split()[0])
            #     time_str = duration_parts[1]
            #     # Convert the time string to a datetime object
            #     dt = datetime.strptime(time_str, '%H:%M:%S.%f')
            #     # Add the number of days to the datetime object
            #     dt += timedelta(days=days)
            #     # Format the datetime as a string in "hh:mm:ss" format
            #     time_str_formatted = dt.strftime('%H:%M:%S')

            # print(date_object.strftime("%z"))
            Task.objects.filter(Q(task_name=i.task_name) & Q(user__email=email)).update(time_diff=time_diff)
            #save only when object is created
        zero_duration = timedelta(seconds=0)
        print('sero_dur,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',zero_duration)
        # now=datetime.now()
        # date_string = now.strftime('%Y-%m-%dT%H:%M')
        # date_object = datetime.strptime(date_string , '%Y-%m-%dT%H:%M')
        today = time.strftime("%Y-%m-%d")
        now=datetime.now()
        print('///////////',today)
        time_str = now.strftime('%H:%M')
        print(',,,,,,,,,,,,,,,,,,,,',time_str)
        return Task.objects.all().filter(Q(user__email=email) & Q(time_diff__gte=zero_duration) ).order_by('task_date')


    @staticmethod
    def get_overdue_task(email):
        zero_duration = timedelta(seconds=0)
        # now=datetime.now()
        # date_string = now.strftime('%Y-%m-%dT%H:%M')
        # date_object = datetime.strptime(date_string , '%Y-%m-%dT%H:%M')
        today = time.strftime("%Y-%m-%d")
        now=datetime.now()
        time_str = now.strftime('%H:%M')
        return Task.objects.all().filter(Q(user__email=email) & Q(time_diff__lt=zero_duration) ).order_by('-task_date')
        #lte for less or equal to

    @staticmethod
    def get_overdue_task_delete(email):
        zero_duration = timedelta(seconds=0)
        today = time.strftime("%Y-%m-%d")
        now=datetime.now()
        time_str = now.strftime('%H:%M')
        Task.objects.all().filter(Q(user__email=email) & Q(time_diff__gt=zero_duration)  | (Q(task_date__date=today) &  Q(task_date__time__lte=time_str)) ).delete()
        #lte for less or equal to

    @staticmethod
    def task_delete_by_name(email,task_name):
        Task.objects.all().filter(Q(user__email=email) & Q(task_name=task_name)).delete()
        #lte for less or equal to

    @staticmethod
    def count_user_task(email):
        return Task.objects.all().filter(user__email=email).count()


 