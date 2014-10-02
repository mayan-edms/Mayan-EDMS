from __future__ import absolute_import

from django.contrib import admin

from .models import StagingFolder, SourceTransformation, WebForm

admin.site.register(StagingFolder)
admin.site.register(SourceTransformation)
admin.site.register(WebForm)
