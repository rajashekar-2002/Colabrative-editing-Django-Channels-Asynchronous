from django.db import models
# from notebook.models import Notebook
# from notes.models import Notes

# Create your models here.
class User(models.Model):
    email=models.EmailField(unique=True, max_length=30,null=False,blank=False)
    password=models.CharField(max_length=20,null=False,blank=False)


    def __str__(self):
        return self.email


    @staticmethod
    def check_user_exist(email):
        try:
            if User.objects.all().filter(email=email):
                return True
        except:
            return False


    @staticmethod
    def user_object(email):
        try:
            return User.objects.filter(email=email).first()
        except:
            return False


