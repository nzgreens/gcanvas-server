import uuid

from django.db import models
from django.conf import settings



class Address(models.Model):
    address_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address1 = models.CharField(max_length=50, null=False)
    address2 = models.CharField(max_length=50, blank=True, null=True)
    address3 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50, blank=True)
    zip = models.CharField(max_length=50)
    lat = models.FloatField()
    lng = models.FloatField()
    


class Person(models.Model):
    external_id = models.IntegerField(unique=True, blank=True, null=True)
    person_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    occupation = models.CharField(max_length=50, blank=True, null=True)
    sex = models.CharField(max_length=10, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    primary_address = models.ForeignKey('Address')
    contact_status_id = models.IntegerField(blank=True, null=True)
    support_level = models.IntegerField(blank=True, null=True)
    is_volunteer = models.BooleanField(default=False)
    host_billboard = models.BooleanField(default=False)
   


class UserPersonAssignment(models.Model):
    user_person_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    person = models.OneToOneField(Person)
    seen = models.BooleanField(default=False)
    
