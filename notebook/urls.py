from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('notebook/',views.notebook,name='notebook'),
    
    path('new_notebook/',views.new_notebook,name='new_notebook'),
    path('share-notebook/',views.share_notebook,name='share-notebook'),
    path('share-with-me-notebook/',views.share_with_me_notebook,name='shared_with_me'),
    path('notebook/<str:bookmark>/',views.bookmark,name='bookmark'),
    path('sort/<str:sort>/',views.sort,name='bookmark'),
    path('showtags/',views.showtags,name='showtag'),
   path('searchall/',views.searchall,name='searchall'),

    # path('notebook/home/<str:variable>/',views.home_tabs,name='home_tabs'),
   
  
]
