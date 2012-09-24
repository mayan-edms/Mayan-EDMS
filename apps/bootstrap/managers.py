from __future__ import absolute_import

import logging

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from django.db import models
from django.core import management

from .classes import BootstrapModel
from .literals import COMMAND_DUMPDATA

logger = logging.getLogger(__name__)


class BootstrapSetupManager(models.Manager):
    def explode(self, data):
        """
        Gets a compressed and compacted bootstrap setup and creates a new
        database BootstrapSetup instance
        """
        pass

    def dump(cls, format):
        models = [instance.get_fullname() for instance in BootstrapModel.get_all()]
        logger.debug('models: %s' % models)
        result = StringIO()
        options = dict(indent=4, format=format, use_natural_keys=True, interactive=False, verbosity=0, stdout=result)
        management.call_command(COMMAND_DUMPDATA, *models, **options)
        result.seek(0)
        logger.debug('result: %s' % result)
        return result.read()         
