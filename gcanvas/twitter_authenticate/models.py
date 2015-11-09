from django.db import models

from django.conf import settings

#from django.contrib.auth.models import User

class TwitterUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    twitter_id = models.CharField(max_length=255)
    twitter_screen_name = models.CharField(max_length=255)
    oauth_token_secret = models.CharField(max_length=255)
    oauth_token = models.CharField(max_length=255)


class UserResources(models.Model):
    owner_key = models.CharField(max_length=256)
    owner_secret = models.CharField(max_length=256)
    
