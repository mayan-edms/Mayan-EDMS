import logging

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(name=__name__)


class ErrorLoggingMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        logger.exception(
            'Exception caught by request middleware; %s, %s', request,
            exception
        )
