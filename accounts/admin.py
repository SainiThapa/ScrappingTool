from django.contrib import admin

from accounts.models import BaseUser, SuperUser

# Register your models here.

admin.site.register(SuperUser)
admin.site.register(BaseUser)
