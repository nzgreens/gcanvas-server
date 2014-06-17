from django.db import models
from django.contrib.auth.models import User


#this will do, don't'need to create a custom user
class NationBuilderUser(models.Model):
    nation_user_id = models.IntegerField(unique=True)
    oauth_token = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User)
    
