from django.urls import path
from . import views
urlpatterns = [
   
    path('<slug>',views.notes_by_notebook,name='notes'),
    path('<slug:notebook>/content/<slug:note>',views.selectnotes,name='selectnotes'),
    path('search/',views.notes_search,name='notessearch'),
    path('tags/',views.tags,name="tags"),
    path('delete_tag/',views.delete_tag,name='delete_tag'),
    path('content/',views.content,name='content'),
    path('<slug>/bookmark/<str:bookmark>/',views.bookmark_notes,name='bookmark_notes'),
    path('attachment/',views.attachment,name='attachment'),
    path('delete_img/',views.delete_img,name='delete_img'),
    path('new_notes/',views.new_notes,name='new_notes'),
    path('sort/',views.sort,name='sort_notes'),
    # path('save_imgage/',views.save_image,name='save_imgage'),
    # path('<slug:notebook>/content/<slug:note>/?<str:qstr>',views.delete_tag,name='delete_tag'),
]



# use name field not to overlap same urls
# BOUT SLUG
# https://vegibit.com/slug-based-routing-in-django/


# ICONS CSS
# https://www.w3schools.com/icons/fontawesome5_icons_social.asp