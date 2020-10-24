from django.contrib import admin

from .models.document_models import DeletedDocument, Document
from .models.document_file_models import DocumentFile
from .models.document_file_page_models import DocumentFilePage
from .models.document_type_models import DocumentType, DocumentTypeFilename
from .models.misc_models import DuplicatedDocument, RecentDocument


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


@admin.register(DeletedDocument)
class DeletedDocumentAdmin(admin.ModelAdmin):
    date_hierarchy = 'deleted_date_time'
    list_filter = ('document_type',)
    list_display = ('uuid', 'label', 'document_type', 'deleted_date_time')
    readonly_fields = ('uuid', 'document_type')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_added'
    inlines = (DocumentFileInline,)
    list_filter = ('document_type', 'is_stub')
    list_display = ('uuid', 'label', 'document_type', 'date_added', 'is_stub')
    readonly_fields = ('uuid', 'document_type', 'date_added')


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    inlines = (DocumentTypeFilenameInline,)
    list_display = (
        'label', 'trash_time_period', 'trash_time_unit', 'delete_time_period',
        'delete_time_unit'
    )


@admin.register(DuplicatedDocument)
class DuplicatedDocumentAdmin(admin.ModelAdmin):
    list_display = (
        'document', 'datetime_added'
    )


@admin.register(RecentDocument)
class RecentDocumentAdmin(admin.ModelAdmin):
    date_hierarchy = 'datetime_accessed'
    list_display = ('user', 'document', 'datetime_accessed')
    list_display_links = ('document', 'datetime_accessed')
    list_filter = ('user',)
    readonly_fields = ('user', 'document', 'datetime_accessed')
