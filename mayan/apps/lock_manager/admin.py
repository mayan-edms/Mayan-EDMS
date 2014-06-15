from __future__ import absolute_import

from django.contrib import admin

from .models import Lock


class LockAdmin(admin.ModelAdmin):
    model = Lock


admin.site.register(Lock, LockAdmin)
