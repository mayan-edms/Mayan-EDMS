from django.contrib import admin

from .models import (
    StagingFolderSource, WatchFolderSource, WebFormSource
)

admin.site.register(StagingFolderSource)
admin.site.register(WatchFolderSource)
admin.site.register(WebFormSource)
