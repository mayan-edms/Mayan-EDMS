from __future__ import unicode_literals

from dateutil.parser import parse


class MetadataValidator(object):
    _registry = []

    @classmethod
    def register(cls, parser):
        cls._registry.append(parser)

    @classmethod
    def get_all(cls):
        return cls._registry

    @classmethod
    def get_import_path(cls):
        return cls.__module__ + '.' + cls.__name__

    @classmethod
    def get_import_paths(cls):
        return [validator.get_import_path() for validator in cls.get_all()]

    def parse(self, input_data):
        raise NotImplementedError


class DateAndTimeValidator(MetadataValidator):
    def validate(self, input_data):
        return parse(input_data).isoformat()


class DateValidator(MetadataValidator):
    def validate(self, input_data):
        return parse(input_data).date().isoformat()


class TimeValidator(MetadataValidator):
    def validate(self, input_data):
        return parse(input_data).time().isoformat()


MetadataValidator.register(DateAndTimeValidator)
MetadataValidator.register(DateValidator)
MetadataValidator.register(TimeValidator)
