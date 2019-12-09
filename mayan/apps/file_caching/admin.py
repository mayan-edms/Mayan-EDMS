from __future__ import unicode_literals

from django.contrib import admin

from .models import Cache


@admin.register(Cache)
class CacheAdmin(admin.ModelAdmin):
    list_display = ('name', 'label', 'storage_instance_path', 'maximum_size')
