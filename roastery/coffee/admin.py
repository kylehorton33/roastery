from django.contrib import admin

from .models import Bean, Extraction, Roast

# Register your models here.
admin.site.register(Bean)
admin.site.register(Roast)
admin.site.register(Extraction)
