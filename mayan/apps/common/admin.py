from django.contrib import admin

from .models import ErrorLogEntry, UserLocaleProfile


@admin.register(ErrorLogEntry)
class ErrorLogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'datetime'
    list_display = ('namespace', 'content_object', 'datetime', 'result')
    readonly_fields = list_display


@admin.register(UserLocaleProfile)
class UserLocaleProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'timezone', 'language',)
    list_filter = ('timezone', 'language')
    search_fields = (
        'user__username', 'user__first_name', 'user__last_name',
        'user__email', 'timezone',
    )
