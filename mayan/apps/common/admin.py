from __future__ import unicode_literals

from django.contrib import admin

from .models import SharedUploadedFile, UserLocaleProfile


@admin.register(SharedUploadedFile)
class SharedUploadedFileAdmin(admin.ModelAdmin):
    date_hierarchy = 'datetime'
    list_display = ('file', 'filename', 'datetime',)
    readonly_fields = list_display


@admin.register(UserLocaleProfile)
class UserLocaleProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'timezone', 'language',)
    list_filter = ('timezone', 'language')
    search_fields = (
        'user__username', 'user__first_name', 'user__last_name',
        'user__email', 'timezone',
    )
