from __future__ import absolute_import


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
