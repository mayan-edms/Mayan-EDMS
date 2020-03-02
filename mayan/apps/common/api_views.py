from __future__ import absolute_import, unicode_literals

from django.contrib.contenttypes.models import ContentType

from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from mayan.apps.rest_api import viewsets

from .classes import Template
from .serializers import ContentTypeSerializer, TemplateSerializer


class ContentTypeAPIViewSet(viewsets.MayanReadOnlyModelAPIViewSet):
    filter_backends = ()
    lookup_url_kwarg = 'content_type_id'
    permission_classes = ()
    queryset = ContentType.objects.order_by('app_label', 'model')
    serializer_class = ContentTypeSerializer

    @swagger_auto_schema(
        operation_description='Retrieve a list of all the content types.'
    )
    def list(self, *args, **kwargs):
        return super(ContentTypeAPIViewSet, self).list(*args, **kwargs)

    @swagger_auto_schema(
        operation_description=(
            'Retrieve the details of the selected content type.'
        )
    )
    def retrieve(self, *args, **kwargs):
        return super(ContentTypeAPIViewSet, self).retrieve(*args, **kwargs)


class TemplateAPIViewSet(viewsets.MayanReadOnlyModelAPIViewSet):
    lookup_url_kwarg = 'template_name'
    permission_classes = (IsAuthenticated,)
    serializer_class = TemplateSerializer

    def get_object(self):
        return Template.get(
            self.kwargs['template_name']
        ).render(request=self.request)

    def get_queryset(self):
        return Template.all(rendered=True, request=self.request)

    @swagger_auto_schema(
        operation_description='Retrieve a list of all templates.'
    )
    def list(self, *args, **kwargs):
        return super(TemplateAPIViewSet, self).list(*args, **kwargs)

    @swagger_auto_schema(
        operation_description='Retrieve the details of the selected template.'
    )
    def retrieve(self, *args, **kwargs):
        return super(TemplateAPIViewSet, self).retrieve(*args, **kwargs)
