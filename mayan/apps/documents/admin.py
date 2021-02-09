from django.contrib import admin

from .models.document_models import Document
from .models.document_file_models import DocumentFile
from .models.document_file_page_models import DocumentFilePage
from .models.document_type_models import DocumentType, DocumentTypeFilename
from .models.recently_accessed_document_models import RecentlyAccessedDocument
from .models.trashed_document_models import TrashedDocument


class DocumentFilePageInline(admin.StackedInline):
    model = DocumentFilePage
    extra = 1
    classes = ('collapse-open',)
    allow_add = True


class DocumentTypeFilenameInline(admin.StackedInline):
    model = DocumentTypeFilename
    extra = 1
    classes = ('collapse-open',)
    allow_add = True


class DocumentFileInline(admin.StackedInline):
    model = DocumentFile
    extra = 1
    classes = ('collapse-open',)
    allow_add = True


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    date_hierarchy = 'datetime_created'
    inlines = (DocumentFileInline,)
    list_filter = ('document_type', 'is_stub')
    list_display = ('uuid', 'label', 'document_type', 'datetime_created', 'is_stub')
    readonly_fields = ('uuid', 'document_type', 'datetime_created')


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    inlines = (DocumentTypeFilenameInline,)
    list_display = (
        'label', 'trash_time_period', 'trash_time_unit', 'delete_time_period',
        'delete_time_unit'
    )


@admin.register(RecentlyAccessedDocument)
class RecentlyAccessedDocumentAdmin(admin.ModelAdmin):
    date_hierarchy = 'datetime_accessed'
    list_display = ('user', 'document', 'datetime_accessed')
    list_display_links = ('document', 'datetime_accessed')
    list_filter = ('user',)
    readonly_fields = ('user', 'document', 'datetime_accessed')


@admin.register(TrashedDocument)
class TrashedDocumentAdmin(admin.ModelAdmin):
    date_hierarchy = 'trashed_date_time'
    list_filter = ('document_type',)
    list_display = ('uuid', 'label', 'document_type', 'trashed_date_time')
    readonly_fields = ('uuid', 'document_type')
