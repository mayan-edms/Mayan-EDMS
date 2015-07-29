from __future__ import unicode_literals

from django.contrib import admin

from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = 'submit_date'
    list_display = ('document', 'submit_date', 'user', 'comment')
    readonly_fields = ('document', 'submit_date', 'user', 'comment')


admin.site.register(Comment, CommentAdmin)
