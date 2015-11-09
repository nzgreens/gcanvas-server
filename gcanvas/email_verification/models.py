from django.db import models

from django.contrib.auth.models import User

class EmailVerified(models.Model):
#    user = models.ForeignKey(User)
    code = models.CharField(max_length=150, null=True)
    valid = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
