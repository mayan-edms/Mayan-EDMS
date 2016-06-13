from __future__ import unicode_literals

from django.contrib import admin

from organizations.admin import OrganizationAdminMixin

from .models import Folder


@admin.register(Folder)
class FolderAdmin(OrganizationAdminMixin, admin.ModelAdmin):
    filter_horizontal = ('documents',)
    list_display = ('label', 'datetime_created')
    list_display_links = ('label',)
