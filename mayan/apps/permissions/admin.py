from __future__ import unicode_literals

from django.contrib import admin

from .models import StoredPermission, Role


class StoredPermissionAdmin(admin.ModelAdmin):
    list_display = ('namespace', 'name')
    list_display_links = list_display


admin.site.register(StoredPermission, StoredPermissionAdmin)
admin.site.register(Role)
