from __future__ import absolute_import

from django.contrib import admin

from .models import StagingFolder, WebForm, SourceTransformation

admin.site.register(StagingFolder)
admin.site.register(WebForm)
admin.site.register(SourceTransformation)
