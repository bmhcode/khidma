from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe # pip install markupsafe

class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True, verbose_name=_('username'))
    email = models.EmailField(blank=True, null=True, verbose_name=_('email'))
    image = models.ImageField(blank=True, null=True, upload_to='users/', default='user.jpg', verbose_name=_('Image')) #,default='media/placeholder.png')
    bio = models.CharField(max_length=100, blank=True, verbose_name=_('bio'))
    
    USERNAME_FIELD = "username"
    # REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username 
    
    def user_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('full name'))
    phone = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('phone'))
    verified = models.BooleanField(default=False, verbose_name=_('verified')) 
    
    def __str__(self):
        return self.full_name
    
class ContactUs(models.Model):
    full_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=254)
    phone = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural= 'Contact Us'

    def __str__(self):
        return self.full_name
    