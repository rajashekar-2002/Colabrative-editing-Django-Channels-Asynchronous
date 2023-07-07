from django.db import models
from autoslug import AutoSlugField
from signin.models import User
from django.db.models import Q
# from notes.models import Notes


# Create your models here.


#pip install django-autoslug
class Notebook(models.Model):
    book_name=models.CharField(null=False,max_length=25)
    book_created_on=models.DateTimeField(auto_now_add=True)
    book_last_modified = models.DateTimeField(auto_now=True)
    notebook_slug=AutoSlugField(populate_from='book_name')
    bookmark_notebook=models.BooleanField(default=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        unique_together=[['book_name','user']]

    def __str__(self):
        return self.book_name

    def get_all_notebook():
        return Notebook.objects.all()


    @staticmethod
    def check_notebook(name,email):
        check=Notebook.objects.all().filter(Q(book_name=name) & Q(user__email=email))
        if check:
            return True
        return False




    @staticmethod
    def user_notebook(email):
        return Notebook.objects.all().filter(user__email=email)
        # not user=email get error return int

    @staticmethod
    def user_notebook_count(email):
        return Notebook.objects.all().filter(user__email=email).count()


    @staticmethod
    def check_user_and_notebook_exist(notebook,user):
        try:
            if Notebook.objects.all().filter(Q(user__email=user) & ~Q(book_name=notebook)):
                return User.objects.filter(email=user).first()
        except:
            return None


    @staticmethod
    def get_notebook(notebook,email):
        return Notebook.objects.filter(Q(notebook_slug=notebook),Q(user__email=email)).first()

    # @staticmethod
    # def user_notes(email):
    #     return Notes.objects.all().filter(notebook__user=email)


    # @staticmethod
    # def user_notes_recent_updated(email):
    #     return Notes.objects.all().filter(notebook__user=email).order_by('notes_last_modified')
    #     # Notes.objects.all().order_by('notes_last_modified')


class Shared_with_me(models.Model):
    email=models.CharField(max_length=20,null=True,blank=True,default='@gmail.com')
    notebook_name=models.CharField(max_length=20,null=True,default=None)
    notebook_slug=AutoSlugField(populate_from='notebook_name',default='slug')
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    # notebook=models.ForeignKey(Notebook,on_delete=models.CASCADE,related_name='share')
    shared_by=models.CharField(max_length=20,null=False,default='@gmail.com')


    @staticmethod
    def update_shared_with_me(notebook,email,user_object,user_mail,notebook_slug):
        object=Shared_with_me(email=email,notebook_name=notebook,notebook_slug=notebook_slug,user=user_object,shared_by=user_mail)
        object.save()
        return

    @staticmethod
    def return_shared_notebook(email):
        return Shared_with_me.objects.all().filter(user__email=email)

        