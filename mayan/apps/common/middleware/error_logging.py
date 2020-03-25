import logging

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(name=__name__)


class ErrorLoggingMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if not isinstance(exception, (PermissionDenied, Http404)):
            # Don't log non critical exceptions
            logger.exception(
                'Exception caught by request middleware; %s, %s', request,
                exception
            )
