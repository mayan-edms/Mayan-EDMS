from __future__ import absolute_import

from django.contrib import admin

from .models import StoredPermission, PermissionHolder, Role, RoleMember


class PermissionHolderInline(admin.StackedInline):
    model = PermissionHolder
    extra = 1
    classes = ('collapse-open',)
    allow_add = True


class PermissionAdmin(admin.ModelAdmin):
    inlines = [PermissionHolderInline]
    list_display = ('namespace', 'name')
    list_display_links = list_display


class RoleMemberInline(admin.StackedInline):
    model = RoleMember
    extra = 1
    classes = ('collapse-open',)
    allow_add = True


class RoleAdmin(admin.ModelAdmin):
    inlines = [RoleMemberInline]


admin.site.register(StoredPermission, PermissionAdmin)
admin.site.register(Role, RoleAdmin)
