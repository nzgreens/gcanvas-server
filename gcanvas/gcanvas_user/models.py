from django.db import models

from django.contrib.auth.models import User

from email_verification.models import EmailVerified

class GCanvasUser(models.Model):
    validated = models.ForeignKey(EmailVerified)
    user = models.ForeignKey(User)
