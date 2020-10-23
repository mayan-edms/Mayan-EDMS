from django.contrib import admin

from .models import Theme, UserThemeSetting


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('label',)
    search_fields = ('label',)


@admin.register(UserThemeSetting)
class UserThemeSettingAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme',)
    list_filter = ('theme__label',)
    search_fields = (
        'user__username', 'user__first_name', 'user__last_name',
        'user__email', 'theme__label',
    )
