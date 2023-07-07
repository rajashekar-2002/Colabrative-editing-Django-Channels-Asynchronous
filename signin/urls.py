from django.urls import path
from . import views
urlpatterns = [
    path('signin/',views.signin,name='signin'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout,name='logout'),
    path('verifyotp/',views.verifyotp,name='verifyotp'),
    path('altsignup/',views.altsignup,name='altsignup'),
]
