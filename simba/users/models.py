from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    UserClass = models.CharField("user class",max_length=50,null=True,unique=False,default='N/A')
    Client = models.CharField("client",max_length=50,null=True,unique=False,default='N/A')
    Carrier = models.CharField("carrier",max_length=50,null=True,unique=False,default='N/A')
    Salary = models.CharField("salary",max_length=50,null=True,unique=False,default='N/A')
    UserClientAccess = models.CharField("UserClientAccess",max_length=255,null=True,unique=False,default='N/A')

def __str__(self):
    return self.user.username