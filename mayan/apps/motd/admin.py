from __future__ import unicode_literals

from django.contrib import admin

from .models import MessageOfTheDay


@admin.register(MessageOfTheDay)
class MessageOfTheDayAdmin(admin.ModelAdmin):
    list_display = ('label', 'enabled', 'start_datetime', 'end_datetime')
