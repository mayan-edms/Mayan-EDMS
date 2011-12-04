'''Views file for the rest_api app'''

import logging

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from documents.models import Document, DocumentVersion, DocumentPage
from converter.exceptions import UnknownFileFormat, UnkownConvertError

from djangorestframework.views import View, ModelView, ListModelView, InstanceModelView
from djangorestframework.mixins import InstanceMixin, ReadModelMixin
from djangorestframework.response import Response
from djangorestframework import status

logger = logging.getLogger(__name__)


class ReadOnlyInstanceModelView(InstanceModelView):
    allowed_methods = ['GET']


class APIBase(View):
    """This is the REST API for Mayan EDMS (https://github.com/rosarior/mayan/).

    All the API calls can be navigated either through the browser or from the command line...

        bash: curl -X GET http://127.0.0.1:8000/api/                           # (Use default renderer)
        bash: curl -X GET http://127.0.0.1:8000/api/ -H 'Accept: text/plain'   # (Use plaintext documentation renderer)

    """

    def get(self, request):
        return [
            {'name': 'Version 0 Alpha', 'url': reverse('api-version-0')}
        ]


class Version_0(View):
    def get(self, request):
        return [
            {'name': 'Resources', 'resources': ['document/<pk>']}
        ]


class IsZoomable(View):
    def get(self, request, pk, page_number, version_pk):
        logger.info('received is_zoomable call from: %s' % (request.META['REMOTE_ADDR']))
        document_version = get_object_or_404(DocumentVersion, pk=version_pk)
        try:
            document_version.document.get_image_cache_name(int(page_number), version_pk)
            return {'result': True}
        except (UnknownFileFormat, UnkownConvertError,
            DocumentPage.DoesNotExist, Document.DoesNotExist,
            DocumentVersion.DoesNotExist):
            return {'result': False}
