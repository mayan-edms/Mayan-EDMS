from __future__ import absolute_import

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import JobQueue, JobQueueItem


class JobQueueItemInline(admin.StackedInline):
    model = JobQueueItem


class JobQueueAdmin(admin.ModelAdmin):
    model = JobQueue
    list_display = ('name', 'label', 'total_items')
    inlines = [JobQueueItemInline]

    def total_items(self, obj):
        return obj.items.all().count()
    total_items.short_description = _(u'total items')


admin.site.register(JobQueue, JobQueueAdmin)
