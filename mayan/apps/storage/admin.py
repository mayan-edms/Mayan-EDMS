from django.contrib import admin

from .models import DownloadFile, SharedUploadedFile


@admin.register(DownloadFile)
class DownloadFileAdmin(admin.ModelAdmin):
    date_hierarchy = 'datetime'
    list_display = ('file', 'filename', 'datetime',)
    readonly_fields = list_display


@admin.register(SharedUploadedFile)
class SharedUploadedFileAdmin(admin.ModelAdmin):
    date_hierarchy = 'datetime'
    list_display = ('file', 'filename', 'datetime',)
    readonly_fields = list_display
