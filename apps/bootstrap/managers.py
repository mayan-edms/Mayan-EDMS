from __future__ import absolute_import

import logging

from django.db import models
from django.core import serializers

from .classes import BootstrapModel
from .literals import FIXTURE_TYPE_FIXTURE_PROCESS, FIXTURE_TYPE_EMPTY_FIXTURE

logger = logging.getLogger(__name__)


class BootstrapSetupManager(models.Manager):
    def explode(self, data):
        """
        Gets a compressed and compacted bootstrap setup and creates a new
        database BootstrapSetup instance
        """
        pass

    def dump(self, serialization_format):
        """
        Get the current setup of Mayan in bootstrap format fixture
        """
        result = []
        for bootstrap_model in BootstrapModel.get_all(sort_by_dependencies=True):
            model_fixture = bootstrap_model.dump(serialization_format)
            # Only add non empty model fixtures
            if not FIXTURE_TYPE_EMPTY_FIXTURE[serialization_format](model_fixture):
                result.append(model_fixture)
        return FIXTURE_TYPE_FIXTURE_PROCESS[serialization_format]('\n'.join(result))
