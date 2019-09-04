from __future__ import unicode_literals

import logging

from PIL import Image
from pyzbar.pyzbar import decode
import qrcode

from django.apps import apps
from django.db import transaction
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.translation import string_concat, ugettext_lazy as _

from mayan.apps.common.serialization import yaml_dump, yaml_load
from mayan.apps.documents.literals import DOCUMENT_IMAGE_TASK_TIMEOUT
from mayan.apps.documents.tasks import task_generate_document_page_image

from .literals import (CONTROL_CODE_MAGIC_NUMBER, CONTROL_CODE_SEPARATOR)

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class ControlCode(object):
    _registry = {}
    arguments = ()

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def get_label(cls):
        if cls.arguments:
            return string_concat(cls.label, ': ', ', '.join(cls.arguments))
        else:
            return cls.label

    @classmethod
    def get_choices(cls):
        return sorted(
            [
                (name, klass.get_label()) for name, klass in cls._registry.items()
            ]
        )

    @classmethod
    def process_document_version(cls, document_version):
        logger.info(
            'Starting processing document version: %s', document_version
        )

        for document_page in document_version.pages.all():
            task = task_generate_document_page_image.apply_async(
                kwargs=dict(
                    document_page_id=document_page.pk
                )
            )

            cache_filename = task.get(
                timeout=DOCUMENT_IMAGE_TASK_TIMEOUT, disable_sync_subtasks=False
            )

            with document_page.cache_partition.get_file(filename=cache_filename).open() as file_object:
                image = Image.open(file_object)
                for code in decode(image):
                    logger.debug('code found: %s', code)
                    parts = code.data.split(CONTROL_CODE_SEPARATOR)

                    if parts[0] == CONTROL_CODE_MAGIC_NUMBER:
                        try:
                            control_code_class = ControlCode.get(name=parts[2])
                        except KeyError:
                            # Unknown control code name
                            pass
                        else:
                            document_page.enabled = False
                            document_page.save()

                            arguments = CONTROL_CODE_SEPARATOR.join(parts[3:])
                            control_code = control_code_class(
                                **yaml_load(arguments)
                            )
                            control_code.execute()

    @classmethod
    def register(cls, control_code):
        cls._registry[control_code.name] = control_code

    def __init__(self, **kwargs):
        self.kwargs = {}
        for argument_name in self.arguments:
            setattr(self, argument_name, kwargs.get(argument_name))
            self.kwargs[argument_name] = kwargs.get(argument_name)

    def __str__(self):
        return '{} {}'.format(self.label, self.kwargs)

    def get_image(self, order=0):
        return qrcode.make(self.get_qrcode_string(order=order))

    def get_qrcode_string(self, order=0):
        result = []
        result.append(CONTROL_CODE_MAGIC_NUMBER)
        result.append(force_text(order))
        result.append(self.name)
        result.append(
            yaml_dump(
                data=self.kwargs, allow_unicode=True, default_flow_style=True
            )
        )

        return CONTROL_CODE_SEPARATOR.join(result)

    def execute(self):
        raise NotImplementedError(
            'Your %s class has not defined the required '
            'execue() method.' % self.__class__.__name__
        )
