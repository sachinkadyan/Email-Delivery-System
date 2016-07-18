from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import AbstractUser
from mail import models as mail_models

# Create your models here.
class MyUser(AbstractUser):
	userID = models.AutoField(max_length=50, primary_key=True)
	dob = models.DateField()
	messages = models.ManyToManyField(mail_models.Message, related_name='received_by')