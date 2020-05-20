import logging

from django.apps import apps
from django.db import transaction

from mayan.apps.common.classes import PropertyHelper

from .events import event_file_metadata_document_version_finish
from .exceptions import FileMetadataDriverError
from .signals import post_document_version_file_metadata_processing

logger = logging.getLogger(name=__name__)


class FileMetadataHelper(PropertyHelper):
    @staticmethod
    @property
    def constructor(*args, **kwargs):
        return FileMetadataHelper(*args, **kwargs)

    def get_result(self, name):
        name = name.replace('_', '.')
        result = self.instance.get_file_metadata(dotted_name=name)
        return result


class FileMetadataDriver(object):
    _registry = {}

    @classmethod
    def process_document_version(cls, document_version):
        # Get list of drivers for the document's MIME type
        driver_classes = cls._registry.get(document_version.mimetype, ())
        # Add wilcard drivers, drivers meant to be executed for all MIME types.
        driver_classes = driver_classes + tuple(cls._registry.get('*', ()))

        for driver_class in driver_classes:
            try:
                driver = driver_class()

                driver.initialize()

                with transaction.atomic():
                    driver.process(document_version=document_version)
                    event_file_metadata_document_version_finish.commit(
                        action_object=document_version.document,
                        target=document_version
                    )

                    transaction.on_commit(
                        lambda: post_document_version_file_metadata_processing.send(
                            sender=document_version.__class__,
                            instance=document_version
                        )
                    )
            except FileMetadataDriverError:
                # If driver raises error, try next in the list
                pass
            else:
                # If driver was successfull there is no need to try
                # others in the list for this mimetype
                return

    @classmethod
    def register(cls, mimetypes):
        for mimetype in mimetypes:
            cls._registry.setdefault(mimetype, []).append(cls)

    def get_driver_path(self):
        return '.'.join([self.__module__, self.__class__.__name__])

    def initialize(self):
        StoredDriver = apps.get_model(
            app_label='file_metadata', model_name='StoredDriver'
        )

        driver_path = self.get_driver_path()

        self.driver_model, created = StoredDriver.objects.get_or_create(
            driver_path=driver_path, defaults={
                'internal_name': self.internal_name
            }
        )

    def process(self, document_version):
        logger.info(
            'Starting processing document version: %s', document_version
        )

        self.driver_model.driver_entries.filter(
            document_version=document_version
        ).delete()

        document_version_driver_entry = self.driver_model.driver_entries.create(
            document_version=document_version
        )

        results = self._process(document_version=document_version) or {}

        for key, value in results.items():
            document_version_driver_entry.entries.create(
                key=key, value=value
            )

    def _process(self, document_version):
        raise NotImplementedError(
            'Your %s class has not defined the required '
            'process_document_version() method.' % self.__class__.__name__
        )
