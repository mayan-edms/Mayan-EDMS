from __future__ import unicode_literals

from django.contrib import admin

from organizations.admin import OrganizationAdminMixin

from .models import MetadataType


@admin.register(MetadataType)
class MetadataTypeAdmin(OrganizationAdminMixin, admin.ModelAdmin):
    list_display = (
        'name', 'label', 'default', 'lookup', 'validation', 'parser'
    )
