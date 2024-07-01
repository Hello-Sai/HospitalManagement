from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class User(AbstractUser):
    profile = models.CharField(max_length=10,choices=(('Doctor',"doctor"),('Patient','patient')))
    profile_picture = models.ImageField()
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','password']
    address = models.TextField()

    objects = CustomUserManager()

class Doctor(models.Model):
    profile = models.OneToOneField(User,on_delete=models.CASCADE)


class Patient(models.Model):
    profile = models.OneToOneField(User,on_delete=models.CASCADE)
    
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save,sender=User)
def create_account(sender,instance=None,created=False,**kwargs):
    if created:
        print(instance.profile)
        if instance.profile=="Doctor":
            Doctor.objects.create(profile=instance)
            # print("He is doctor")
        else:
            Patient.objects.create(profile=instance)
            # print("He is patient")

class Blog(models.Model):
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name="blogs")
    title = models.CharField(max_length=20)
    image = models.ImageField(upload_to='blogs/')
    category =models.CharField(max_length=2,choices=(('MH','Mental Health'), ('HD','Heart Disease'), ('CD','Covid19'), ('IZ','Immunization')))
    summary = models.TextField()
    content = models.TextField()
    is_drafted = models.BooleanField(default=False)

    def save(self,*args,**kwargs):
        
        
        words = self.summary.strip().split()[:15]
        truncated_summary = ' '.join(words)
        self.summary = truncated_summary

        super().save(*args, **kwargs)
        
