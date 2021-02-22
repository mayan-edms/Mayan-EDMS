import logging

from django.apps import apps

from mayan.apps.common.classes import PropertyHelper

from .events import event_file_metadata_document_file_finish
from .exceptions import FileMetadataDriverError
from .signals import signal_post_document_file_file_metadata_processing

logger = logging.getLogger(name=__name__)


class FileMetadataHelper(PropertyHelper):
    @staticmethod
    @property
    def constructor(*args, **kwargs):
        return FileMetadataHelper(*args, **kwargs)

    def get_result(self, name):
        result = self.instance.get_file_metadata(dotted_name=name)
        return result


class FileMetadataDriver:
    _registry = {}

    @classmethod
    def process_document_file(cls, document_file):
        # Get list of drivers for the document's MIME type
        driver_classes = cls._registry.get(document_file.mimetype, ())
        # Add wilcard drivers, drivers meant to be executed for all MIME types.
        driver_classes = driver_classes + tuple(cls._registry.get('*', ()))

        for driver_class in driver_classes:
            try:
                driver = driver_class()

                driver.initialize()

                driver.process(document_file=document_file)

                signal_post_document_file_file_metadata_processing.send(
                    sender=document_file.__class__,
                    instance=document_file
                )

                event_file_metadata_document_file_finish.commit(
                    action_object=document_file.document,
                    target=document_file
                )

            except FileMetadataDriverError:
                """If driver raises error, try next in the list."""
            else:
                # If driver was successful there is no need to try
                # others in the list for this mimetype.
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

    def process(self, document_file):
        logger.info(
            'Starting processing document file: %s', document_file
        )

        self.driver_model.driver_entries.filter(
            document_file=document_file
        ).delete()

        document_file_driver_entry = self.driver_model.driver_entries.create(
            document_file=document_file
        )

        results = self._process(document_file=document_file) or {}

        for key, value in results.items():
            document_file_driver_entry.entries.create(
                key=key, value=value
            )

    def _process(self, document_file):
        raise NotImplementedError(
            'Your %s class has not defined the required '
            '_process() method.' % self.__class__.__name__
        )
