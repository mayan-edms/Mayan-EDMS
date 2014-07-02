"""Views file for the rest_api app"""
from __future__ import absolute_import

import logging

from django.utils.translation import ugettext_lazy as _

from rest_framework import generics
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .classes import EndPoint

logger = logging.getLogger(__name__)

registered_version_0_endpoints = [
]


class APIBase(generics.GenericAPIView):
    def get(self, request, format=None):
        return Response([
            {'name': 'Version 0', 'url': reverse('api-version-0', request=request, format=format)}
        ])


class Version_0(generics.GenericAPIView):
    def get(self, request, format=None):
        return Response({
            'endpoints': [
                {'name': unicode(endpoint), 'url': reverse('api-version-0-endpoint', args=[unicode(endpoint)], request=request, format=format)} for endpoint in EndPoint.get_all()
            ],
        })

class EndPointView(generics.GenericAPIView):
    def get(self, request, endpoint_name, format=None):
        result = []

        endpoint = EndPoint.get(endpoint_name)
        for service in endpoint.services:
            result.append(
                {
                    'description': service['description'],
                    'name': service['urlpattern'].name,
                    'url': service['url'],
                }
            )

        return Response({
            'services': result
        })
