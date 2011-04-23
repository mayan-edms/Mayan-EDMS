from django.contrib import admin

from permissions.models import Permission, PermissionHolder, Role, RoleMember


class PermissionHolderInline(admin.StackedInline):
    model = PermissionHolder
    extra = 1
    classes = ('collapse-open',)
    allow_add = True


class PermissionAdmin(admin.ModelAdmin):
    inlines = [PermissionHolderInline]
    list_display = ('namespace', 'name', 'label')
    list_display_links = list_display


class RoleMemberInline(admin.StackedInline):
    model = RoleMember
    extra = 1
    classes = ('collapse-open',)
    allow_add = True


class RoleAdmin(admin.ModelAdmin):
    inlines = [RoleMemberInline]


admin.site.register(Permission, PermissionAdmin)
admin.site.register(Role, RoleAdmin)
