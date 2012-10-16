from __future__ import absolute_import

import logging

import requests

from django.db import models
from django.core import serializers

from .classes import BootstrapModel, FixtureMetadata
from .literals import (FIXTURE_TYPE_FIXTURE_PROCESS, FIXTURE_TYPE_EMPTY_FIXTURE)

logger = logging.getLogger(__name__)


class BootstrapSetupManager(models.Manager):
    def dump(self, serialization_format):
        """
        Get the current setup of Mayan in bootstrap format fixture
        """
        result = []
        logger.debug('start dumping data')
        for bootstrap_model in BootstrapModel.get_all(sort_by_dependencies=True):
            logger.debug('dumping model: %s' % bootstrap_model.get_fullname())
            model_fixture = bootstrap_model.dump(serialization_format)
            # Only add non empty model fixtures
            if not FIXTURE_TYPE_EMPTY_FIXTURE[serialization_format](model_fixture):
                result.append(model_fixture)
        return FIXTURE_TYPE_FIXTURE_PROCESS[serialization_format]('\n'.join(result))

    def import_setup(self, file_data):
        BootstrapModel.check_magic_number(file_data)
        metadata = FixtureMetadata.read_all(file_data)
        instance = self.model(fixture=file_data, **metadata)
        instance.save(update_metadata=False)

    def import_from_file(self, files):
        file_data = files.read()
        self.import_setup(file_data)
        
    def import_from_url(self, url):
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            self.import_setup(response.text)
        else:
            response.raise_for_status()
