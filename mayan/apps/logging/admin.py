from django.contrib import admin

from .models import ErrorLog, ErrorLogPartition, ErrorLogPartitionEntry


class ReadOnlyAdminMixin:
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ErrorLogPartitionEntryInline(admin.TabularInline):
    model = ErrorLogPartitionEntry


class ErrorLogPartitionInline(admin.StackedInline):
    classes = ('collapse-open',)
    model = ErrorLogPartition


@admin.register(ErrorLog)
class ErrorLogAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    inlines = (ErrorLogPartitionInline,)
    list_display = ('name', 'app_label')
    readonly_fields = list_display


@admin.register(ErrorLogPartition)
class ErrorLogPartitionAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    inlines = (ErrorLogPartitionEntryInline,)
    list_display = ('name', 'error_log')
    readonly_fields = list_display
