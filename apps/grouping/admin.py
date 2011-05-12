from django.contrib import admin

from grouping.models import DocumentGroup, DocumentGroupItem


class DocumentGroupItemInline(admin.StackedInline):
    model = DocumentGroupItem
    extra = 1
    classes = ('collapse-open',)
    allow_add = True


class DocumentGroupAdmin(admin.ModelAdmin):
    inlines = [DocumentGroupItemInline]
    
admin.site.register(DocumentGroup, DocumentGroupAdmin)
