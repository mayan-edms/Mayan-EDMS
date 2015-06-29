from __future__ import unicode_literals

from django.contrib import admin

from .models import AccessEntry


class AccessEntryAdmin(admin.ModelAdmin):
    model = AccessEntry
    list_display = ('pk', 'role', 'permission', 'content_object')
    list_display_links = ('pk',)
    related_lookup_fields = {
        'generic': (('content_type', 'object_id'),),
    }

admin.site.register(AccessEntry, AccessEntryAdmin)
