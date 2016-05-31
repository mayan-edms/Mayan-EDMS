from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.utils.translation import ugettext_lazy as _

from organizations.admin import OrganizationAdminMixin

from .models import MayanGroup, MayanUser


@admin.register(MayanUser)
class MayanUserAdmin(OrganizationAdminMixin, UserAdmin):
    list_display_links = ('username',)


@admin.register(MayanGroup)
class MayanGroupAdmin(OrganizationAdminMixin, GroupAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
