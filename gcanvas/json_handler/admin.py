from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(UserPersonAssignment)
admin.site.register(Person)
admin.site.register(Address)
