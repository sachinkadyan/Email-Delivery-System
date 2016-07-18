from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Message(models.Model):
	messageID = models.AutoField(primary_key=True)
	subject = models.CharField(max_length=50)
	body = models.CharField(max_length=255)
	timestamp = models.DateTimeField(auto_now_add=True)
	sender = models.ForeignKey('account.MyUser')