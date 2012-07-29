from django.contrib import admin

from django.utils.translation import ugettext_lazy as _

from queue_manager.models import Queue, QueueItem


class QueueItemInline(admin.StackedInline):
    model = QueueItem


class QueueAdmin(admin.ModelAdmin):
    model = Queue
    list_display = ('name', 'label', 'total_items')
    inlines = [QueueItemInline]

    def total_items(self, obj):
        return obj.items.all().count()
    total_items.short_description = _(u'total items')


admin.site.register(Queue, QueueAdmin)
