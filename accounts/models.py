from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
# Create your models here.
    
from django.dispatch import receiver
from django.db.models.signals import post_save

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
    profile_picture = models.ImageField(upload_to="Images/")
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','password']
    address = models.TextField()
    is_doctor = models.BooleanField(default=False)
    objects = CustomUserManager()

@receiver(post_save,sender=User)
def create_account(sender,instance=None,created=False,**kwargs):
    if created:
        print(instance.profile)
        if instance.profile=="Doctor":
            instance.is_doctor = True
            instance.save()
            # print("He is doctor")


def user_path(instance,filename):
    return f"{instance.user.username}_blog/{filename}"
class Blog(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="blogs")
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to=user_path)
    category =models.CharField(max_length=15,choices=(('cancer','cancer'), ('diarrhoea','Diarrhoea'),('typhoid','Typhoid'), ('malaria','Malaria'), ))
    summary = models.TextField(blank=True)
    content = models.TextField(blank=True)
    is_drafted = models.BooleanField(default=False)

    def save(self,*args,**kwargs):

        super().save(*args, **kwargs)
        
