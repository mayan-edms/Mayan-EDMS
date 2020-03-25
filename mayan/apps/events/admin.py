from django.contrib import admin

from .models import EventSubscription, Notification, StoredEventType


@admin.register(EventSubscription)
class EventSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'stored_event_type')


@admin.register(StoredEventType)
class StoredEventTypeAdmin(admin.ModelAdmin):
    readonly_fields = ('name', '__str__')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'read')
