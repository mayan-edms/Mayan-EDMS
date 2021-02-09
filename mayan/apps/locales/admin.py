from django.contrib import admin

from .models import UserLocaleProfile


@admin.register(UserLocaleProfile)
class UserLocaleProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'timezone', 'language',)
    list_filter = ('timezone', 'language')
    search_fields = (
        'user__username', 'user__first_name', 'user__last_name',
        'user__email', 'timezone',
    )
