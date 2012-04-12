from django.contrib import admin

from dynamic_search.models import RecentSearch, IndexableObject


class RecentSearchAdmin(admin.ModelAdmin):
    list_display = ('user', 'query', 'datetime_created', 'hits')
    list_display_links = ('user', 'query', 'datetime_created', 'hits')
    readonly_fields = ('user', 'query', 'datetime_created', 'hits')

admin.site.register(RecentSearch, RecentSearchAdmin)
admin.site.register(IndexableObject)
