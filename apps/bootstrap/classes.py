from __future__ import absolute_import

from django.db import models

from .exceptions import ExistingData


class Cleanup(object):
    """
    Class to store all the registered cleanup functions in one place
    """
    _registry = {}

    @classmethod
    def execute_all(cls):
        for cleanup in cls._registry.values():
            cleanup.function()

    def __init__(self, name, function):
        self.name = name
        self.function = function
        self.__class__._registry[self.name] = self


class BootstrapModel(object):
    """
    Class used to keep track of all the models to be dumped to create a
    bootstrap setup from the current setup in use
    """
    _registry = {}

    @classmethod
    def check_for_data(cls):
        for model in cls.get_all():
            model_instance = models.get_model(model.app_name, model.model_name)
            if model_instance.objects.all().count():
                raise ExistingData

    @classmethod
    def get_all(cls):
        return cls._registry.values()

    def get_fullname(self):
        return '.'.join([self.app_name, self.model_name])

    def __init__(self, model_name, app_name=None):
        app_name_splitted = None
        if '.' in model_name:
            app_name_splitted, model_name = model_name.split('.')
        
        self.app_name = app_name_splitted or app_name
        if not self.app_name:
            raise Exception('Pass either a dotted app plus model name or a model name and a separate app name')
        self.model_name = model_name
        self.__class__._registry[self.get_fullname()] = self
