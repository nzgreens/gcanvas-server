import logging
import uuid

from django.db import models

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class GCanvasUserManager(BaseUserManager):
    def create_user(self, username, firstname, lastname, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        if not username:
            raise ValueError('Users must have a username')

        if not firstname:
            raise ValueError('Users must have a firstname')

        if not lastname:
            raise ValueError('Users must have a lastname')

        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            username=username,
            firstname=firstname,
            lastname=lastname,
            email=self.normalize_email(email)
        )

        if password is not None:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, firstname, lastname, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class GCanvasUser(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    validated = models.BooleanField(default=False)
    firstname = models.CharField(max_length=40)
    lastname = models.CharField(max_length=40)
    email = models.EmailField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = GCanvasUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['firstname', 'lastname', 'email']

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):              # __unicode__ on Python 2
        return "%(firstname)s %(lastname)s <%(email)s" % {'firstname': self.firstname, 'lastname': self.lastname, 'email': self.email}

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



class GCanvasUserVerification(models.Model):
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    


#gcanvas_user.GCanvasUserVerification.user: (fields.W342) Setting unique=True on a ForeignKey has the same effect as using a OneToOneField.
#	HINT: ForeignKey(unique=True) is usually better served by a OneToOneField.
