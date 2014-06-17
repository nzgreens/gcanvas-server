from django.db import models


class Address(models.Model):
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50)
    address3 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=50)
    lat = models.FloatField()
    lng = models.FloatField()
    


class People(models.Model):
    nation_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    occupation = models.CharField(max_length=50)
    sex = models.CharField(max_length=10)
    birthdate = models.DateField(null=True)
    note = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=50)
    primary_address = models.ForeignKey('Address')
    contact_status_id = models.IntegerField(null=True)
    support_level = models.IntegerField(null=True)
    is_volunteer = models.BooleanField(default=False)
    host_billboard = models.BooleanField(default=False)
   
