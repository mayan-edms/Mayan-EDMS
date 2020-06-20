from django.contrib import admin

from mayan.apps.common.admin_mixins import ReadOnlyAdminMixin

from .models import ErrorLog, ErrorLogPartition, ErrorLogPartitionEntry


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
    list_display = ('name', 'error_log', 'get_model_instance')
    readonly_fields = list_display
