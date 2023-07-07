from django.urls import path
from . import views
urlpatterns = [
    path('',views.collabrate,name='collabrate'),
    path('addgroup/',views.addgrp,name='new_colab_grp'),
    path('group/<str:grpname>/',views.selectgrp,name='selectgrp'),
    path('addparticipants/',views.addpart,name='addparticipants'),
    path('savenote/',views.savenote,name='savecolabnote'),
   
   
  
]