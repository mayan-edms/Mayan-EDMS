from django.contrib import admin

from tags.models import TagProperties


#class PermissionAdmin(admin.ModelAdmin):
#    inlines = [PermissionHolderInline]
#    list_display = ('namespace', 'name', 'label')
#    list_display_links = list_display

admin.site.register(TagProperties)
