from __future__ import unicode_literals

from django.contrib import admin

from .models import LogEntry


class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'datetime'
    list_display = ('datetime', 'message')
    readonly_fields = ('datetime', 'message')


admin.site.register(LogEntry, LogEntryAdmin)
