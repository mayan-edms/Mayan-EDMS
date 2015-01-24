from django.contrib import admin

from .models import (
    SourceTransformation, StagingFolderSource, WatchFolderSource,
    WebFormSource
)

admin.site.register(SourceTransformation)
admin.site.register(StagingFolderSource)
admin.site.register(WatchFolderSource)
admin.site.register(WebFormSource)
