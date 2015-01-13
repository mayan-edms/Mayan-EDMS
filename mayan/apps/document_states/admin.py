from django.contrib import admin

from .models import Workflow, WorkflowState, WorkflowTransition


class WorkflowStateInline(admin.TabularInline):
    model = WorkflowState


class WorkflowTransitionInline(admin.TabularInline):
    model = WorkflowTransition


class WorkflowAdmin(admin.ModelAdmin):
    inlines = [WorkflowStateInline, WorkflowTransitionInline]


admin.site.register(Workflow, WorkflowAdmin)
