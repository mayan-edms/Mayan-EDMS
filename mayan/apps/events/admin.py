from django.contrib import admin

from .models import EventType

class EventTypeAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'get_label')


admin.site.register(EventType, EventTypeAdmin)
