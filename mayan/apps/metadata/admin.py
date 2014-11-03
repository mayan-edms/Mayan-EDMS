from __future__ import absolute_import

from django.contrib import admin

from .models import MetadataType


class MetadataTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'default', 'lookup')


admin.site.register(MetadataType, MetadataTypeAdmin)
