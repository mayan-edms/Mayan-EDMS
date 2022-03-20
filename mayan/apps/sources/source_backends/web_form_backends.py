import logging

from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from rest_framework import status
from rest_framework.generics import get_object_or_404 as rest_get_object_or_404
from rest_framework.response import Response

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models.document_type_models import DocumentType
from mayan.apps.documents.permissions import permission_document_create
from mayan.apps.storage.models import SharedUploadedFile

from ..classes import SourceBackendAction, SourceBackend
from ..forms import WebFormUploadFormHTML5
from ..tasks import task_process_document_upload

from .mixins import (
    SourceBackendCompressedMixin, SourceBackendInteractiveMixin,
    SourceBaseMixin
)

__all__ = ('SourceBackendWebForm',)
logger = logging.getLogger(name=__name__)


class SourceBackendWebForm(
    SourceBackendCompressedMixin, SourceBackendInteractiveMixin,
    SourceBaseMixin, SourceBackend
):
    actions = (
        SourceBackendAction(
            name='upload', arguments=(
                'document_type_id', 'expand'
            ), accept_files=True
        ),
    )
    label = _('Web form')
    upload_form_class = WebFormUploadFormHTML5

    def action_upload(self, document_type_id, file, request, expand=False):
        queryset = AccessControlList.objects.restrict_queryset(
            queryset=DocumentType.objects.all(),
            permission=permission_document_create,
            user=request.user
        )

        document_type = rest_get_object_or_404(
            queryset=queryset, pk=document_type_id
        )

        self.process_kwargs = {
            'request': request
        }

        shared_uploaded_file = SharedUploadedFile.objects.create(
            file=file
        )

        kwargs = {
            'callback_kwargs': self.get_callback_kwargs(),
            'document_type_id': document_type.pk,
            'expand': expand,
            'shared_uploaded_file_id': shared_uploaded_file.pk,
            'source_id': self.model_instance_id,
            'user_id': request.user.pk
        }

        task_process_document_upload.apply_async(kwargs=kwargs)

        return None, Response(status=status.HTTP_202_ACCEPTED)

    def get_shared_uploaded_files(self):
        return (
            SharedUploadedFile.objects.create(
                file=self.process_kwargs['forms']['source_form'].cleaned_data['file']
            ),
        )

    def get_view_context(self, context, request):
        return {
            'subtemplates_list': [
                {
                    'name': 'appearance/generic_multiform_subtemplate.html',
                    'context': {
                        'forms': context['forms'],
                        'is_multipart': True,
                        'form_action': '{}?{}'.format(
                            reverse(
                                viewname=request.resolver_match.view_name,
                                kwargs=request.resolver_match.kwargs
                            ), request.META['QUERY_STRING']
                        ),
                        'form_css_classes': 'dropzone',
                        'form_disable_submit': True,
                        'form_id': 'html5upload',
                    },
                }
            ]
        }
