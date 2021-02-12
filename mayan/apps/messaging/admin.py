from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('date_time', 'sender_object', 'user', 'subject', 'read')
