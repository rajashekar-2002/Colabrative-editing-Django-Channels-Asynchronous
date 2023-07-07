from django.urls import path
from . import views

urlpatterns = [
    path('',views.task,name='task'),
    path('add-task/',views.add_task,name='add_task'),
    path('delete-overdue-task/',views.delete_overdue_task,name='delete_overdue'),
    path('delete_task/<str:task_name>',views.delete_task,name='delete_task'),
   
]
