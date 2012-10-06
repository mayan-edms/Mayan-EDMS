from __future__ import absolute_import

import logging

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
        for bootstrap_model in BootstrapModel.get_all():
            model_fixture = bootstrap_model.dump(serialization_format)
            if '[]' not in model_fixture and '{}' not in model_fixture:
                result.append(model_fixture)
        return '\n'.join(result)
