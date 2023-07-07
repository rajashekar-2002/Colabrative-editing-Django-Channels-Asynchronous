from django.contrib import admin
from . models import Notes
from .models import Attachment
# Register your models here.

@admin.register(Notes)
class AdminNotes(admin.ModelAdmin):
    list_display=['notes_name','notes_created_on','notes_last_modified','tags','notebook','notes_slug','bookmark_notes']


@admin.register(Attachment)
class AdminAttachment(admin.ModelAdmin):
    list_display=['attach','notes']