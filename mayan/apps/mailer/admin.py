from django.contrib import admin

from .models import UserMailer


@admin.register(UserMailer)
class UserMailerAdmin(admin.ModelAdmin):
    list_display = (
        'label', 'default', 'enabled', 'backend_path', 'backend_data'
    )
