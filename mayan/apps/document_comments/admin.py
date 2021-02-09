from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = 'submit_date'
    list_display = ('document', 'submit_date', 'user', 'text')
    list_filter = ('user',)
    readonly_fields = ('document', 'submit_date', 'user', 'text')
    search_fields = ('text',)
