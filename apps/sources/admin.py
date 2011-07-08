from django.contrib import admin

from sources.models import StagingFolder, WebForm, SourceTransformation


admin.site.register(StagingFolder)
admin.site.register(WebForm)
admin.site.register(SourceTransformation)
