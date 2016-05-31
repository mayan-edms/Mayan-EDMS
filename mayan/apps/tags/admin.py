from __future__ import unicode_literals

from django.contrib import admin

from organizations.admin import OrganizationAdminMixin

from .models import Tag


@admin.register(Tag)
class TagAdmin(OrganizationAdminMixin, admin.ModelAdmin):
    filter_horizontal = ('documents',)
    list_display = ('label', 'color')
    list_display_links = ('label',)
