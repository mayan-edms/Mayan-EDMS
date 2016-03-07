from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from user_management.models import MayanUser


@admin.register(MayanUser)
class MayanUserAdmin(UserAdmin):
    list_display = ('organization',) + UserAdmin.list_display
    list_display_links = ('username',)
    list_filter = UserAdmin.list_filter + ('organization',)
    ordering = ('organization',) + UserAdmin.ordering
    fieldsets = UserAdmin.fieldsets
    fieldsets[1][1]['fields'] = ('organization',) + fieldsets[1][1]['fields']
