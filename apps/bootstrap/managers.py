from __future__ import absolute_import

import logging

import requests

from django.db import models
from django.core import serializers
from django.utils.simplejson import loads
from django.db import IntegrityError
from django.db.models import Q

from .classes import BootstrapModel, FixtureMetadata
from .literals import (FIXTURE_TYPE_FIXTURE_PROCESS, FIXTURE_TYPE_EMPTY_FIXTURE,
    BOOTSTRAP_REPOSITORY_URL, BOOTSTRAP_REPOSITORY_INDEX_FILE)

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

    def import_setup(self, file_data, overwrite=False):
        BootstrapModel.check_magic_number(file_data)
        metadata = FixtureMetadata.read_all(file_data)
        instance = self.model(fixture=file_data, **metadata)
        try:
            instance.save(update_metadata=False)
        except IntegrityError:
            if not overwrite:
                raise
            else:
                # Delete conflicting bootstrap setups
                query = Q()
                if 'slug' in metadata:
                    query = query | Q(slug=metadata['slug'])

                if 'name' in metadata:
                    query = query | Q(name=metadata['name'])

                self.model.objects.filter(query).delete()
                self.import_setup(file_data)

    def import_from_file(self, files):
        file_data = files.read()
        self.import_setup(file_data)
        
    def import_from_url(self, url, **kwargs):
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            self.import_setup(response.text, **kwargs)
        else:
            response.raise_for_status()

    def repository_sync(self):
        response = requests.get('%s/%s' % (BOOTSTRAP_REPOSITORY_URL, BOOTSTRAP_REPOSITORY_INDEX_FILE))
        if response.status_code == requests.codes.ok:
            for entry in loads(response.text):
                bootstrap_setup_url = '%s/%s' % (BOOTSTRAP_REPOSITORY_URL, entry['filename'])
                self.import_from_url(bootstrap_setup_url, overwrite=True)
        else:
            response.raise_for_status()
        
