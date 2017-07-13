from __future__ import unicode_literals

import logging

logger = logging.getLogger(__name__)


class ErrorLoggingMiddleware(object):
    def process_exception(self, request, exception):
        logger.exception(
            'Exception caught by request middleware; %s, %s', request,
            exception
        )
