from __future__ import absolute_import

from django.contrib import admin

from .models import AccessEntry


#class PermissionHolderInline(admin.StackedInline):
#    model = PermissionHolder
#    extra = 1
#    classes = ('collapse-open',)
#    allow_add = True#
#
class AccessEntryAdmin(admin.ModelAdmin):
    related_lookup_fields = {
        'generic': [['holder_type', 'holder_id'], ['content_type', 'object_id']],
    }
    #inlines = [PermissionHolderInline]
    list_display = ('pk', 'holder_object', 'permission', 'content_object')
    list_display_links = ('pk',)
    model = AccessEntry

admin.site.register(AccessEntry, AccessEntryAdmin)
