import logging

from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mayan.apps.storage.models import SharedUploadedFile

from ..classes import SourceBackend
from ..forms import WebFormUploadFormHTML5

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
    label = _('Web form')
    upload_form_class = WebFormUploadFormHTML5

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

    def get_shared_uploaded_files(self):
        return (
            SharedUploadedFile.objects.create(
                file=self.process_kwargs['forms']['source_form'].cleaned_data['file']
            ),
        )
