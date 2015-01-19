from __future__ import unicode_literals

from django.contrib import admin

from .models import Workflow, WorkflowInstance, WorkflowState, WorkflowTransition


class WorkflowStateInline(admin.TabularInline):
    model = WorkflowState


class WorkflowTransitionInline(admin.TabularInline):
    model = WorkflowTransition


class WorkflowAdmin(admin.ModelAdmin):
    inlines = [WorkflowStateInline, WorkflowTransitionInline]


class WorkflowInstanceAdmin(admin.ModelAdmin):
    list_display = ('workflow', 'document')


admin.site.register(Workflow, WorkflowAdmin)
admin.site.register(WorkflowInstance, WorkflowInstanceAdmin)
