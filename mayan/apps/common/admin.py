from __future__ import unicode_literals

from django.contrib import admin

from .models import AutoAdminSingleton, SharedUploadedFile

admin.site.register(AutoAdminSingleton)
admin.site.register(SharedUploadedFile)
