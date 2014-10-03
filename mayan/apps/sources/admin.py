from __future__ import absolute_import

from django.contrib import admin

from .models import StagingFolderSource, SourceTransformation, WebFormSource

admin.site.register(StagingFolderSource)
admin.site.register(SourceTransformation)
admin.site.register(WebFormSource)
