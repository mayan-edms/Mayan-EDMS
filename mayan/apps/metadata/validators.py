from __future__ import unicode_literals

from dateutil.parser import parse


class MetadataParser(object):
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
        return [parser.get_import_path() for parser in cls.get_all()]

    def parse(self, input_data):
        raise NotImplementedError


class DateAndTimeParser(MetadataParser):
    def parse(self, input_data):
        return parse(input_data).isoformat()


class DateParser(MetadataParser):
    def parse(self, input_data):
        return parse(input_data).date().isoformat()


class TimeParser(MetadataParser):
    def parse(self, input_data):
        return parse(input_data).time().isoformat()


MetadataParser.register(DateAndTimeParser)
MetadataParser.register(DateParser)
MetadataParser.register(TimeParser)
