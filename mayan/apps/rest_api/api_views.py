from __future__ import unicode_literals

from rest_framework import generics, renderers
from rest_framework.authtoken.views import ObtainAuthToken


class BrowseableObtainAuthToken(ObtainAuthToken):
    """
    Obtain an API authentication token.
    """

    renderer_classes = (renderers.BrowsableAPIRenderer, renderers.JSONRenderer)
