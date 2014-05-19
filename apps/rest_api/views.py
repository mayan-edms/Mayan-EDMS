"""Views file for the rest_api app"""

import logging

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from converter.exceptions import UnknownFileFormat, UnkownConvertError
from documents.models import Document, DocumentVersion, DocumentPage

from rest_framework import generics
from rest_framework import permissions
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .resources import DocumentResourceSimple

logger = logging.getLogger(__name__)


class APIBase(generics.GenericAPIView):
    """This is the REST API for Mayan EDMS (https://github.com/mayan-edms/mayan-edms).

    All the API calls can be navigated either through the browser or from the command line...

        bash: curl -X GET http://127.0.0.1:8000/api/                           # (Use default renderer)
        bash: curl -X GET http://127.0.0.1:8000/api/ -H 'Accept: text/plain'   # (Use plaintext documentation renderer)

    """

    def get(self, request, format=None):
        return Response(
            {'versions': [
                {'name': 'Version 1', 'url': reverse('api-version-1', request=request, format=format), 'number': 1}
            ]}
        )


class Version_1(generics.GenericAPIView):
    def get(self, request, format=None):
        return Response(
            [
                {'name': 'Resources', 'resources': ['document/<pk>']}
            ]
        )


class DocumentDetailView(generics.RetrieveAPIView):
    allowed_methods = ['GET']
    serializer_class = DocumentResourceSimple
    queryset = Document.objects.all()


class IsZoomable(generics.GenericAPIView):
    def get(self, request, pk, page_number, version_pk):
        logger.info('received is_zoomable call from: %s' % (request.META['REMOTE_ADDR']))
        document_version = get_object_or_404(DocumentVersion, pk=version_pk)
        try:
            document_version.document.get_image_cache_name(int(page_number), version_pk)
            return Response({'result': True})
        except (UnknownFileFormat, UnkownConvertError,
            DocumentPage.DoesNotExist, Document.DoesNotExist,
            DocumentVersion.DoesNotExist):
            return Response({'result': False})
