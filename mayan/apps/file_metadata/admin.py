from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import StoredDriver


@admin.register(StoredDriver)
class StoredDriverAdmin(admin.ModelAdmin):
    list_display = ('internal_name', 'get_label', 'driver_path')

    def get_label(self, instance):
        return instance.driver_label
    get_label.short_description = _('Label')
