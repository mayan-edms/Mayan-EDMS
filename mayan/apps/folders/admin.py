from __future__ import unicode_literals

from django.contrib import admin

from .models import Folder


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    filter_horizontal = ('documents',)
    list_display = ('label', 'user', 'datetime_created')
    list_filter = ('user',)
