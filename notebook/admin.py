from django.contrib import admin
from .models import Notebook
from .models import Shared_with_me
# Register your models here.

@admin.register(Notebook)
class AdminNotebook(admin.ModelAdmin):
    list_display=['book_name','book_created_on','book_last_modified','notebook_slug','bookmark_notebook','user']

@admin.register(Shared_with_me)
class AdminShared_with_me(admin.ModelAdmin):
    list_display=['email','notebook_name','user','shared_by','notebook_slug']