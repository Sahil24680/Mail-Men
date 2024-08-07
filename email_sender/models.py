from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from  login .models import CustomUser
from django.utils import timezone






class Email(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_emails', default=None)
    To = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_emails',default=None)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    reply_ids = models.ManyToManyField('self', related_name='replies', blank=True, symmetrical=False)
    archived = models.BooleanField(default=False)
    starred= models.BooleanField(default=False)

    def __str__(self):
        return self.sender.email 
   

    
class Inbox(models.Model):
    inbox_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='inbox')
    num_inbox = models.PositiveBigIntegerField(default=0)
    inbox = models.ManyToManyField(Email, related_name='all_emails', blank=True)
    archived_inbox = models.PositiveBigIntegerField(default=0)
    starred_inbox = models.PositiveBigIntegerField(default=0)