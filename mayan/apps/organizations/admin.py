from __future__ import unicode_literals

from django.contrib import admin

from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('label',)
    search_fields = ('label',)
