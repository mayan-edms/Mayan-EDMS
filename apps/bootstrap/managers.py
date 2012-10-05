from __future__ import absolute_import

import logging

#try:
#    from cStringIO import StringIO
#except ImportError:
#    from StringIO import StringIO

from django.db import models
from django.core import serializers

from .classes import BootstrapModel

logger = logging.getLogger(__name__)


class BootstrapSetupManager(models.Manager):
    def explode(self, data):
        """
        Gets a compressed and compacted bootstrap setup and creates a new
        database BootstrapSetup instance
        """
        pass

    def dump(self, serialization_format):
        result = []
        #models = [instance.get_fullname()
        for bootstrap_model in BootstrapModel.get_all():
        #logger.debug('models: %s' % models)
        #options = dict(indent=4, format=format, use_natural_keys=True, interactive=False, verbosity=0, stdout=result)
        #management.call_command(COMMAND_DUMPDATA, *models, **options)
        #logger.debug('result: %s' % result)
            result.append(bootstrap_model.dump(serialization_format))
        #return result.read()         
        return '\n'.join(result)
