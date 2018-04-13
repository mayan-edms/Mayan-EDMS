from __future__ import absolute_import

import logging

from django.utils.encoding import force_text

logger = logging.getLogger(__name__)

try:
    from .local import *  # NOQA
except ImportError as exception:
    if force_text(exception) != 'No module named local' and force_text(exception) != 'No module named \'mayan.settings.local\'':
        logger.error('Error importing user\'s local.py; %s', exception)
        raise
    else:
        logger.info('No local.py settings file. Using defaults.')
else:
    from .base import *  # NOQA
