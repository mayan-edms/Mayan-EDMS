from __future__ import unicode_literals

from django.contrib import admin

from .models import AutoAdminSingleton

admin.site.register(AutoAdminSingleton)
