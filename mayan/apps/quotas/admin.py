from __future__ import unicode_literals

from django.contrib import admin

from .models import Quota


@admin.register(Quota)
class QuotaAdmin(admin.ModelAdmin):
    list_display = (
        'backend_path', 'backend_data', 'enabled', 'editable',
    )

    def has_change_permission(self, request, obj=None):
        if obj:
            return obj.editable
        else:
            return True

    def has_delete_permission(self, request, obj=None):
        if obj:
            return obj.editable
        else:
            return False
