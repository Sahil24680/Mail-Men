from django.db import models

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(max_length = 100,unique =True)
    pfp = models.ImageField(null=True, blank=True, upload_to='images/')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    