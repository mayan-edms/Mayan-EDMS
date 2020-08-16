from __future__ import absolute_import, unicode_literals

import uuid

from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.utils.text import format_lazy


class BaseDocumentFilenameGenerator:
    default = None
    _registry = {}

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def get_choices(cls):
        return sorted(
            [
                (
                    name, format_lazy('{} - {}', klass.label, klass.description)
                ) for name, klass in cls._registry.items()
            ]
        )

    @classmethod
    def get_default(cls):
        for backend in cls._registry.values():
            if backend.default:
                return backend.name

    @classmethod
    def register(cls, klass):
        cls._registry[klass.name] = klass

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def upload_to(self, instance, filename):
        raise NotImplementedError


class OriginalDocumentFilenameGenerator(BaseDocumentFilenameGenerator):
    name = 'original'
    label = _('Original')
    description = _(
        'Keeps the original filename of the uploaded file.'
    )

    def upload_to(self, instance, filename):
        return '{}'.format(instance.document.label)


class UUIDDocumentFilenameGenerator(BaseDocumentFilenameGenerator):
    default = True
    name = 'uuid'
    label = _('UUID')
    description = _(
        'Generate an immutable, random UUID (RFC 4122) for each file.'
    )

    def upload_to(self, instance, filename):
        return force_text(uuid.uuid4())


BaseDocumentFilenameGenerator.register(klass=OriginalDocumentFilenameGenerator)
BaseDocumentFilenameGenerator.register(klass=UUIDDocumentFilenameGenerator)
