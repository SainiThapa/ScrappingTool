from django.contrib import admin

from .models import Newsheadline, Webportal, FeaturedNews

# Register your models here.

admin.site.register(Newsheadline)
admin.site.register(Webportal)
admin.site.register(FeaturedNews)
