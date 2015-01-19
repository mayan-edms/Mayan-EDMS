from __future__ import unicode_literals

from django.contrib import admin

from .models import MetadataType


class MetadataTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'default', 'lookup', 'validation')


admin.site.register(MetadataType, MetadataTypeAdmin)
