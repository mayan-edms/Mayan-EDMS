from __future__ import unicode_literals

from django.contrib import admin

from .models import (
    StagingFolderSource, WatchFolderSource, WebFormSource
)


@admin.register(StagingFolderSource)
class StagingFolderSourceAdmin(admin.ModelAdmin):
    list_display = ('label', 'enabled', 'folder_path', 'preview_width', 'preview_height', 'uncompress', 'delete_after_upload')


@admin.register(WatchFolderSource)
class WatchFolderSourceAdmin(admin.ModelAdmin):
    list_display = ('label', 'enabled', 'folder_path', 'uncompress')


@admin.register(WebFormSource)
class WebFormSourceAdmin(admin.ModelAdmin):
    list_display = ('label', 'enabled', 'uncompress')
