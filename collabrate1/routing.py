from . import consumers
from django.urls import path
websocket_urlpatterns=[
    path('ws/sc/<str:grpname>/<str:email>/',consumers.MySyncConsumer.as_asgi()),
    
]

