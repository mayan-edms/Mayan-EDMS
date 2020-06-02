import base64
import logging
import os
import time

from furl import furl

from django.core.files import File
from django.core.files.base import ContentFile
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.functional import cached_property
from django.utils.six.moves.urllib.parse import quote_plus, unquote_plus

from mayan.apps.converter.transformations import TransformationResize
from mayan.apps.converter.utils import get_converter_class
from mayan.apps.storage.classes import DefinedStorage

from .literals import STORAGE_NAME_SOURCE_STAGING_FOLDER_FILE

logger = logging.getLogger(name=__name__)


class PseudoFile(File):
    def __init__(self, file, name):
        self.name = name
        self.file = file
        self.file.seek(0, os.SEEK_END)
        self.size = self.file.tell()
        self.file.seek(0)


class SourceUploadedFile(File):
    def __init__(self, source, file, extra_data=None):
        self.file = file
        self.source = source
        self.extra_data = extra_data


class StagingFile:
    """
    Simple class to extend the File class to add preview capabilities
    files in a directory on a storage
    """
    def __init__(self, staging_folder, filename=None, encoded_filename=None):
        self.staging_folder = staging_folder
        if encoded_filename:
            self.encoded_filename = str(encoded_filename)
            self.filename = base64.urlsafe_b64decode(
                unquote_plus(self.encoded_filename)
            ).decode('utf8')
        else:
            self.filename = filename
            self.encoded_filename = quote_plus(base64.urlsafe_b64encode(
                filename.encode('utf8')
            ))

    def __str__(self):
        return force_text(self.filename)

    def as_file(self):
        return File(
            file=open(
                file=self.get_full_path(), mode='rb'
            ), name=self.filename
        )

    @property
    def cache_filename(self):
        return '{}{}'.format(self.staging_folder.pk, self.encoded_filename)

    def delete(self):
        self.storage.delete(self.cache_filename)
        os.unlink(self.get_full_path())

    def generate_image(self, *args, **kwargs):
        transformation_list = self.get_combined_transformation_list(*args, **kwargs)

        # Check is transformed image is available
        logger.debug('transformations cache filename: %s', self.cache_filename)

        if self.storage.exists(self.cache_filename):
            logger.debug(
                'staging file cache file "%s" found', self.cache_filename
            )
        else:
            logger.debug(
                'staging file cache file "%s" not found', self.cache_filename
            )
            image = self.get_image(transformations=transformation_list)
            with self.storage.open(name=self.cache_filename, mode='wb+') as file_object:
                file_object.write(image.getvalue())

        return self.cache_filename

    def get_api_image_url(self, *args, **kwargs):
        final_url = furl()
        final_url.args = kwargs
        final_url.path = reverse(
            'rest_api:stagingfolderfile-image', kwargs={
                'staging_folder_pk': self.staging_folder.pk,
                'encoded_filename': self.encoded_filename
            }
        )

        return final_url.tostr()

    def get_combined_transformation_list(self, *args, **kwargs):
        """
        Return a list of transformation containing the server side
        staging file transformation as well as tranformations created
        from the arguments as transient interactive transformation.
        """
        # Convert arguments into transformations
        transformations = kwargs.get('transformations', [])

        # Set sensible defaults if the argument is not specified or if the
        # argument is None
        width = self.staging_folder.preview_width
        height = self.staging_folder.preview_height

        # Generate transformation hash
        transformation_list = []

        # Interactive transformations second
        for transformation in transformations:
            transformation_list.append(transformation)

        if width:
            transformation_list.append(
                TransformationResize(width=width, height=height)
            )

        return transformation_list

    def get_date_time_created(self):
        return time.ctime(os.path.getctime(self.get_full_path()))

    def get_full_path(self):
        return os.path.join(self.staging_folder.folder_path, self.filename)

    def get_image(self, transformations=None):
        cache_filename = self.cache_filename
        file_object = None

        try:
            file_object = open(file=self.get_full_path(), mode='rb')
            converter = get_converter_class()(file_object=file_object)

            page_image = converter.get_page()

            # Since open "wb+" doesn't create files, check if the file
            # exists, if not then create it
            if not self.storage.exists(cache_filename):
                self.storage.save(name=cache_filename, content=ContentFile(content=''))

            with self.storage.open(file=cache_filename, mode='wb+') as file_object:
                file_object.write(page_image.getvalue())
        except Exception as exception:
            # Cleanup in case of error
            logger.error(
                'Error creating staging file cache "%s"; %s',
                cache_filename, exception
            )
            self.storage.delete(cache_filename)
            if file_object:
                file_object.close()
            raise

        for transformation in transformations:
            converter.transform(transformation=transformation)

        result = converter.get_page()
        file_object.close()
        return result

    @cached_property
    def storage(self):
        return DefinedStorage.get(
            name=STORAGE_NAME_SOURCE_STAGING_FOLDER_FILE
        ).get_storage_instance()
