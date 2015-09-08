from __future__ import unicode_literals

from django.contrib import admin

from .models import RecentSearch


@admin.register(RecentSearch)
class RecentSearchAdmin(admin.ModelAdmin):
    date_hierarchy = 'datetime_created'
    list_display = ('user', 'query', 'datetime_created', 'hits')
    list_display_links = ('user', 'query', 'datetime_created', 'hits')
    list_filter = ('user',)
    readonly_fields = ('user', 'query', 'datetime_created', 'hits')
