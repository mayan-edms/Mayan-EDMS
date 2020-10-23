from django.shortcuts import get_object_or_404

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models import Document
from mayan.apps.rest_api import generics

from .models import ResolvedWebLink, WebLink
from .permissions import (
    permission_web_link_create, permission_web_link_delete,
    permission_web_link_edit, permission_web_link_view,
    permission_web_link_instance_view
)
from .serializers import (
    ResolvedWebLinkSerializer, WebLinkSerializer, WritableWebLinkSerializer
)


class APIDocumentViewMixin:
    def get_document(self):
        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_web_link_instance_view,
            queryset=Document.objects.all(), user=self.request.user
        )
        return get_object_or_404(klass=queryset, pk=self.kwargs['pk'])


class APIResolvedWebLinkListView(APIDocumentViewMixin, generics.ListAPIView):
    """
    get: Returns a list of resolved web links for the specified document.
    """
    mayan_object_permissions = {'GET': (permission_web_link_instance_view,)}
    serializer_class = ResolvedWebLinkSerializer

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super().get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'document': self.get_document(),
                }
            )

        return context

    def get_queryset(self):
        return ResolvedWebLink.objects.get_for(
            document=self.get_document(), user=self.request.user
        )


class APIResolvedWebLinkView(APIDocumentViewMixin, generics.RetrieveAPIView):
    """
    get: Return the details of the selected resolved smart link.
    """
    lookup_url_kwarg = 'resolved_web_link_pk'
    mayan_object_permissions = {'GET': (permission_web_link_instance_view,)}
    serializer_class = ResolvedWebLinkSerializer

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super().get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'document': self.get_document(),
                }
            )

        return context

    def get_queryset(self):
        return ResolvedWebLink.objects.get_for(
            document=self.get_document(), user=self.request.user
        )


class APIResolvedWebLinkNavigateView(
    APIDocumentViewMixin, generics.RetrieveAPIView
):
    """
    get: Perform a redirection to the target URL of the selected resolved smart link.
    """
    lookup_url_kwarg = 'resolved_web_link_pk'
    mayan_object_permissions = {'GET': (permission_web_link_instance_view,)}

    def get_queryset(self):
        return ResolvedWebLink.objects.get_for(
            document=self.get_document(), user=self.request.user
        )

    def retrieve(self, request, *args, **kwargs):
        return self.get_object().get_redirect(
            document=self.get_document(), user=self.request.user
        )

    def get_serializer(self):
        return None

    def get_serializer_class(self):
        return None


class APIWebLinkListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the web links.
    post: Create a new web link.
    """
    mayan_object_permissions = {'GET': (permission_web_link_view,)}
    mayan_view_permissions = {'POST': (permission_web_link_create,)}
    queryset = WebLink.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WebLinkSerializer
        elif self.request.method == 'POST':
            return WritableWebLinkSerializer


class APIWebLinkView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected web link.
    get: Return the details of the selected web link.
    patch: Edit the selected web link.
    put: Edit the selected web link.
    """
    lookup_url_kwarg = 'pk'
    mayan_object_permissions = {
        'DELETE': (permission_web_link_delete,),
        'GET': (permission_web_link_view,),
        'PATCH': (permission_web_link_edit,),
        'PUT': (permission_web_link_edit,)
    }
    queryset = WebLink.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WebLinkSerializer
        else:
            return WritableWebLinkSerializer
