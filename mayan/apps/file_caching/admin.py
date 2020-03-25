from django.contrib import admin

from .models import Cache


@admin.register(Cache)
class CacheAdmin(admin.ModelAdmin):
    list_display = ('defined_storage_name', 'maximum_size')
