from __future__ import absolute_import

from django.contrib import admin

from .models import AutoAdminSingleton, SharedUploadedFile

admin.site.register(AutoAdminSingleton)
admin.site.register(SharedUploadedFile)
