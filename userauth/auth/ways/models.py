from django.db import models
from django.contrib.auth.models import AbstractBaseUser , AbstractUser
from django.contrib.auth.signals import user_logged_in,user_logged_out,user_login_failed
from django.dispatch import receiver
from datetime import datetime

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(max_length= 30)
    passwordbfa = models.CharField(max_length = 100 , default = 'ccccccc')
    passwordotp = models.CharField(max_length=100 , default = 'bbbbbb')
    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.username

class bookshaaaa(models.Model):
    name = models.CharField(max_length = 20)
    price = models.IntegerField()
    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=23)
    def __str__(self):
        return self.name
    
class auditentry(models.Model):
    action = models.CharField(max_length = 64)
    ip = models.GenericIPAddressField(null =True)
    user_name = models.CharField(max_length = 64,null=True)
    time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return '{0}-{1}-{2}'.format(self.action,self.user_name,self.ip)
    def __str__(self):
        return '{0}-{1}-{2}'.format(self.action,self.user_name,self.ip)

@receiver(user_logged_in)
def user_logged_in_callback(request,user, **kwargs):
    ip_add = request.META.get('REMOTE_ADDR')
    auditentry.objects.create(user_name = user , ip =ip_add , action = 'logged in' , time = datetime.now())

@receiver(user_logged_out)
def user_logged_out_callback(request,user, **kwargs):
    ip_add = request.META.get('REMOTE_ADDR')
    auditentry.objects.create(user_name = user , ip = ip_add , action = 'logged_out' , time = datetime.now())

@receiver(user_login_failed)
def user_login_failed_callback(request,user, **kwargs):
    ip_add = request.META.get('REMOTE_ADDR')
    auditentry.objects.create(user_name = user , ip = ip_add , action = 'login_failed' , time = datetime.now())

