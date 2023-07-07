from django.contrib import admin
from .models import Group,Collabnote
# Register your models here.
@admin.register(Group)
class AdminGroup(admin.ModelAdmin):
    list_display=['grpname','user','createdby','date','participants']



@admin.register(Collabnote)
class AdminCollabnote(admin.ModelAdmin):
    list_display=['name','content','group','user']
