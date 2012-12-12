from __future__ import absolute_import

import logging
from itertools import chain

from django.db import models
from django.core import serializers
from django.utils.datastructures import SortedDict

from .exceptions import ExistingData, NotABootstrapSetup
from .literals import (FIXTURE_TYPE_PK_NULLIFIER, FIXTURE_TYPE_MODEL_PROCESS,
    FIXTURE_METADATA_REMARK_CHARACTER, BOOTSTRAP_SETUP_MAGIC_NUMBER)
from .utils import toposort2

logger = logging.getLogger(__name__)


class Cleanup(object):
    """
    Class to store all the registered cleanup functions in one place.
    """
    _registry = {}

    @classmethod
    def execute_all(cls):
        for cleanup in cls._registry.values():
            cleanup.function()

    def __init__(self, function):
        self.function = function
        self.__class__._registry[id(self)] = self


class BootstrapModel(object):
    """
    Class used to keep track of all the models to be dumped to create a
    bootstrap setup from the current setup in use.
    """
    _registry = SortedDict()

    @classmethod
    def get_magic_number(cls):
        return '%s %s' % (FIXTURE_METADATA_REMARK_CHARACTER, BOOTSTRAP_SETUP_MAGIC_NUMBER) 

    @classmethod
    def check_magic_number(cls, data):
        if not data.startswith(cls.get_magic_number()):
            raise NotABootstrapSetup

    @classmethod
    def check_for_data(cls):
        for model in cls.get_all():
            model_instance = models.get_model(model.app_name, model.model_name)
            if model_instance.objects.all().count():
                raise ExistingData

    @classmethod
    def get_all(cls, sort_by_dependencies=False):
        """
        Return all boostrap models, sorted by dependencies optionally.
        """
        if not sort_by_dependencies:
            return cls._registry.values()
        else:
            return (cls.get_by_name(name) for name in list(chain.from_iterable(toposort2(cls.get_dependency_dict()))))

    @classmethod
    def get_dependency_dict(cls):
        """
        Return a dictionary where the key is the model name and it's value
        is a list of models upon which it depends.
        """
        result = {}
        for instance in cls.get_all():
            result[instance.get_fullname()] = set(instance.dependencies)

        logger.debug('result: %s' % result)
        return result

    @classmethod
    def get_by_name(cls, name):
        """
        Return a BootstrapModel instance by the fullname of the model it
        represents.
        """
        return cls._registry[name]

    def get_fullname(self):
        """
        Return a the full app name + model name of the model represented
        by the instance.
        """
        return '.'.join([self.app_name, self.model_name])

    def get_model_instance(self):
        """
        Returns an actual Model class instance of the model.
        """
        return models.get_model(self.app_name, self.model_name)

    def __init__(self, model_name, app_name=None, sanitize=True, dependencies=None):
        app_name_splitted = None
        if '.' in model_name:
            app_name_splitted, model_name = model_name.split('.')
        
        self.app_name = app_name_splitted or app_name
        if not self.app_name:
            raise Exception('Pass either a dotted app plus model name or a model name and a separate app name')
        self.model_name = model_name
        self.sanitize = sanitize
        self.dependencies = dependencies if dependencies else []
        self.__class__._registry[self.get_fullname()] = self

    def dump(self, serialization_format):
        result = serializers.serialize(serialization_format, self.get_model_instance().objects.all(), indent=4, use_natural_keys=True)
        logger.debug('result: "%s"' % result)
        if self.sanitize:
            # Remove primary key values
            result = FIXTURE_TYPE_PK_NULLIFIER[serialization_format](result)
        # Do any clean up required on the fixture
        result = FIXTURE_TYPE_MODEL_PROCESS[serialization_format](result)
        return result


class FixtureMetadata(object):
    """
    Class to automatically create and extract metadata from a bootstrap
    fixture.
    """
    _registry = SortedDict()

    @classmethod
    def get_all(cls):
        return cls._registry.values()

    @classmethod
    def generate_all(cls, fixture_instance):
        result = []
        for fixture_metadata in cls.get_all():
            result.append(fixture_metadata.generate(fixture_instance))

        return '\n'.join(result)

    @classmethod
    def read_all(cls, data):
        result = {}
        for instance in cls.get_all():
            single_result = instance.read_value(data)
            if single_result:
                result[instance.property_name] = single_result

        return result

    def __init__(self, literal, generate_function, read_function=None, property_name=None):
        self.literal = literal
        self.generate_function = generate_function
        self.property_name = property_name
        self.read_function = read_function or (lambda x: x)
        self.__class__._registry[id(self)] = self
        
    def get_with_remark(self):
        return '%s %s' % (FIXTURE_METADATA_REMARK_CHARACTER, self.literal)

    def generate(self, fixture_instance):
        return '%s: %s' % (self.get_with_remark(), self.generate_function(fixture_instance))

    def read_value(self, fixture_data):
        if self.property_name:
            for line in fixture_data.splitlines(False):
                if line.startswith(self.get_with_remark()):
                    # TODO: replace the "+ 4" with a space and next character finding algo
                    return self.read_function(line[len(self.literal) + 4:])             
