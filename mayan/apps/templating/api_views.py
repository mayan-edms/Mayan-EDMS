from rest_framework.permissions import IsAuthenticated

from mayan.apps.rest_api import generics

from .classes import AJAXTemplate
from .serializers import AJAXTemplateSerializer


class APITemplateDetailView(generics.RetrieveAPIView):
    """
    Returns the selected partial template details.
    get: Retrieve the details of the partial template.
    """
    serializer_class = AJAXTemplateSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return AJAXTemplate.get(self.kwargs['name']).render(
            request=self.request
        )


class APITemplateListView(generics.ListAPIView):
    """
    Returns a list of all the available templates.
    """
    serializer_class = AJAXTemplateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return AJAXTemplate.all(rendered=True, request=self.request)
