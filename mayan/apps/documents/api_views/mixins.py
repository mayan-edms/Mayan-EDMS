from rest_framework.generics import get_object_or_404

from mayan.apps.acls.models import AccessControlList

from ..models.document_models import Document
from ..models.document_type_models import DocumentType


class ParentObjectDocumentAPIViewMixin:
    def get_document(self, permission=None):
        queryset = Document.valid.all()

        if permission:
            queryset = AccessControlList.objects.restrict_queryset(
                permission=permission, queryset=queryset,
                user=self.request.user
            )

        return get_object_or_404(
            queryset=queryset, pk=self.kwargs['document_id']
        )


class ParentObjectDocumentFileAPIViewMixin(ParentObjectDocumentAPIViewMixin):
    def get_document_file(self, permission=None):
        queryset = self.get_document().files.all()

        if permission:
            queryset = AccessControlList.objects.restrict_queryset(
                permission=permission, queryset=queryset,
                user=self.request.user
            )

        return get_object_or_404(
            queryset=queryset, pk=self.kwargs['document_file_id']
        )


class ParentObjectDocumentFilePageAPIViewMixin(
    ParentObjectDocumentFileAPIViewMixin
):
    def get_document_file_page(self, permission=None):
        queryset = self.get_document_file().pages.all()

        if permission:
            queryset = AccessControlList.objects.restrict_queryset(
                permission=permission, queryset=queryset,
                user=self.request.user
            )

        return get_object_or_404(
            queryset=queryset, pk=self.kwargs['document_file_page_id']
        )


class ParentObjectDocumentTypeAPIViewMixin:
    def get_document_type(self, permission=None):
        queryset = DocumentType.objects.all()

        if permission:
            queryset = AccessControlList.objects.restrict_queryset(
                permission=permission, queryset=queryset,
                user=self.request.user
            )

        return get_object_or_404(
            queryset=queryset, pk=self.kwargs['document_type_id']
        )


class ParentObjectDocumentVersionAPIViewMixin(ParentObjectDocumentAPIViewMixin):
    def get_document_version(self, permission=None):
        queryset = self.get_document().versions.all()

        if permission:
            queryset = AccessControlList.objects.restrict_queryset(
                permission=permission, queryset=queryset,
                user=self.request.user
            )

        return get_object_or_404(
            queryset=queryset, pk=self.kwargs['document_version_id']
        )


class ParentObjectDocumentVersionPageAPIViewMixin(
    ParentObjectDocumentVersionAPIViewMixin
):
    def get_document_version_page(self, permission=None):
        queryset = self.get_document_version().pages.all()

        if permission:
            queryset = AccessControlList.objects.restrict_queryset(
                permission=permission, queryset=queryset,
                user=self.request.user
            )

        return get_object_or_404(
            queryset=queryset, pk=self.kwargs['document_version_page_id']
        )
