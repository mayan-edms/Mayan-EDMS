from django.contrib.contenttypes.models import ContentType

from mayan.apps.rest_api import generics

from .serializers import ContentTypeSerializer


class APIContentTypeList(generics.ListAPIView):
    """
    Returns a list of all the available content types.
    """
    serializer_class = ContentTypeSerializer
    queryset = ContentType.objects.order_by('app_label', 'model')
