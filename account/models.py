from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
	score = models.PositiveSmallIntegerField(default=0, null=False)
	rank = models.PositiveSmallIntegerField(null=True)
	last_auth = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
        email = models.EmailField(null=True)        
	
	user = models.OneToOneField(User)
