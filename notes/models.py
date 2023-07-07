from django.db import models
from notebook.models import Notebook
from autoslug import AutoSlugField
from django.db.models import Q
from signin.models import User

# Create your models here.
class Notes(models.Model):
    notes_name=models.CharField(max_length=20,blank=False)
    notes_text=models.TextField(default='text here...')
    notes_created_on=models.DateTimeField(auto_now_add=True)
    notes_last_modified = models.DateTimeField(auto_now=True)
    tags =models.TextField(max_length=50, blank=True,default='none')
    notebook=models.ForeignKey(Notebook,on_delete=models.CASCADE,related_name='notes')
    notes_slug=AutoSlugField(populate_from='notes_name',default=None)
    bookmark_notes=models.BooleanField(default=False)



    def __str__(self):
        return self.notes_name

    @staticmethod
    def recent_updated_notes(email):
        return Notes.objects.all().filter(notebook__user__email=email).order_by('notes_last_modified')

    @staticmethod
    def get_all_notes():
        return Notes.objects.all()
    
    @staticmethod
    def get_all_user_tags(email):
        return Notes.objects.all().filter(notebook__user__email=email).exclude(Q(tags='none'))


    @staticmethod
    def get_notes_by_name(slug,email):
        try:
            return Notes.objects.all().filter(Q(notebook__notebook_slug=slug) & Q(notebook__user__email=email))
        except:
            return None

    @staticmethod
    def get_notes_by_book_name(slug,email):
        try:
            return Notes.objects.all().filter(Q(notebook__book_name=slug) & Q(notebook__user__email=email))
        except:
            return None
    

    @staticmethod
    def get_content_by_notes(slug,email):
        return Notes.objects.filter(Q(notes_slug=slug) & Q(notebook__user__email=email)).first()

    @staticmethod
    def save_content(notebook_slug,note_slug,email,content):
        Notes.objects.filter( Q(notebook__user__email=email) & Q(notebook__book_name=notebook_slug) & Q(notes_slug=note_slug)).update(notes_text=content)


    @staticmethod
    def get_notes_from_book_note(notebook,note,email):
        object=Notes.objects.filter(Q(notebook__notebook_slug=notebook) & Q(notes_slug=note) & Q(notebook__user__email=email)).first()
        # object.tags += tag
        # object.save()
        # object= Notes.objects.filter(notes_slug=note).first()
        return object




    @staticmethod
    def user_notes(email):
        return Notes.objects.all().filter(notebook__user__email=email)


    @staticmethod
    def user_notes_recent_updated(email):
        return Notes.objects.all().filter(notebook__user__email=email).order_by('notes_last_modified')


class Attachment(models.Model):
    attach=models.FileField(upload_to="attachments",blank=True,null=True)
    notes=models.ForeignKey(Notes,on_delete=models.CASCADE,related_name='notes')
    # user=models.ForeignKey(User,on_delete=models.CASCADE,default=)


    @staticmethod
    def return_notes_attach(note,email):
        try:
            return Attachment.objects.all().filter(Q(notes__notes_name=note) & Q(notes__notebook__user__email=email))
        except:
            return None