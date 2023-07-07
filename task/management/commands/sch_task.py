from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
# scheduler = BackgroundScheduler()
from datetime import datetime, timedelta
from dateutil.parser import parse
from datetime import datetime, timedelta
from django.shortcuts import redirect
from apscheduler.schedulers.background import BackgroundScheduler



    
def pop():


    # session_engine = settings.SESSION_ENGINE
    

    print('bkjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjhere')
    return redirect('task')