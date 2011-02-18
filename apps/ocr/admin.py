from django.contrib import admin

from models import DocumentQueue, QueueDocument


class QueueDocumentInline(admin.StackedInline):
    model = QueueDocument
    extra = 1
    classes = ('collapse-open',)
    allow_add = True
    

class DocumentQueueAdmin(admin.ModelAdmin):
    inlines = [QueueDocumentInline]
    list_display = ('name', 'label', 'state')

  
admin.site.register(DocumentQueue, DocumentQueueAdmin)

