from django.db import models
from signin.models import User
from django.db.models import Q
# Create your models here.
class Group(models.Model):
    grpname=models.CharField(max_length=20)
    description=models.TextField(max_length=50,default=None)
    createdby=models.EmailField(blank=False,default='@gmail.com')
    date=models.DateTimeField(auto_now=True)
    participants=models.TextField(default=None)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=None)

    class Meta:
        unique_together=[['grpname','user']]


    



    def getgrpobj(email,grpname):
        return Group.objects.filter().first()

class Collabnote(models.Model):
    name=models.CharField(max_length=20)
    content=models.TextField()
    group=models.ForeignKey(Group,on_delete=models.CASCADE,default=None)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=None)








    