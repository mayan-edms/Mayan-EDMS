import logging

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(name=__name__)


class ErrorLoggingMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if (settings.TESTING and not isinstance(exception, (PermissionDenied, Http404))) or not settings.TESTING:
            # Don't log non critical exceptions in testing mode.
            logger.exception(
                'Exception caught by request middleware; %s, %s', request,
                exception
            )
