from __future__ import absolute_import

from django.contrib import admin

from .models import TrashedItem


class TrashedItemAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'object_id', 'content_object',)
    list_display_links = ('content_object',)


admin.site.register(TrashedItem, TrashedItemAdmin)
