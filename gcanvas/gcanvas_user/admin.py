from django.contrib import admin

# Register your models here.

from .models import GCanvasUser

@admin.register(GCanvasUser)
class GCanvasUserAdmin(admin.ModelAdmin):
    exclude = ('password',)

