from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import ControlSheet, ControlSheetCode


class ControlSheetCodeInline(admin.StackedInline):
    allow_add = True
    classes = ('collapse-open',)
    extra = 1
    model = ControlSheetCode


@admin.register(ControlSheet)
class ControlSheetAdmin(admin.ModelAdmin):
    inlines = (ControlSheetCodeInline,)
    list_display = ('label', 'get_codes_count')

    def get_codes_count(self, instance):
        return instance.codes.count()
    get_codes_count.short_description = _('Codes')
