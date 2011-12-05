from django.contrib import admin

from lock_manager.models import Lock


class LockAdmin(admin.ModelAdmin):
    model = Lock


admin.site.register(Lock, LockAdmin)
