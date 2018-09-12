from __future__ import unicode_literals

import base64
import logging
import os
import time

from furl import furl

try:
    # Python 2
    from urllib import unquote_plus
except ImportError:
    # Python 3
    from urllib.parse import unquote_plus


from django.core.files import File
from django.core.files.base import ContentFile
from django.urls import reverse
from django.utils.encoding import force_text, python_2_unicode_compatible

from converter import BaseTransformation, TransformationResize, converter_class
from converter.literals import DEFAULT_ROTATION, DEFAULT_ZOOM_LEVEL

from .storages import storage_staging_file_image_cache

logger = logging.getLogger(__name__)


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


@python_2_unicode_compatible
class StagingFile(object):
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
            self.encoded_filename = base64.urlsafe_b64encode(
                filename.encode('utf8')
            )

    def __str__(self):
        return force_text(self.filename)

    def as_file(self):
        return File(
            file=open(self.get_full_path(), mode='rb'), name=self.filename
        )

    @property
    def cache_filename(self):
        return '{}{}'.format(self.staging_folder.pk, self.encoded_filename)

    def delete(self):
        #TODO: delete cached files
        os.unlink(self.get_full_path())

    def generate_image(self, *args, **kwargs):
        transformation_list = self.get_combined_transformation_list(*args, **kwargs)

        cache_filename = '{}-{}'.format(
            self.cache_filename, BaseTransformation.combine(transformation_list)
        )

        # Check is transformed image is available
        logger.debug('transformations cache filename: %s', cache_filename)

        if storage_staging_file_image_cache.exists(cache_filename):
            logger.debug(
                'transformations cache file "%s" found', cache_filename
            )
        else:
            logger.debug(
                'transformations cache file "%s" not found', cache_filename
            )
            image = self.get_image(transformations=transformation_list)
            with storage_staging_file_image_cache.open(cache_filename, 'wb+') as file_object:
                file_object.write(image.getvalue())

            #self.cached_images.create(filename=cache_filename)

        return cache_filename

    def get_api_image_url(self, *args, **kwargs):
        transformations_hash = BaseTransformation.combine(
            self.get_combined_transformation_list(*args, **kwargs)
        )

        kwargs.pop('transformations', None)

        final_url = furl()
        final_url.args = kwargs
        final_url.path = reverse(
            'rest_api:stagingfolderfile-image-view', args=(
                self.staging_folder.pk,
                self.encoded_filename
            )
        )
        final_url.args['_hash'] = transformations_hash

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
        width = kwargs.get('width', self.staging_folder.preview_width) or self.staging_folder.preview_width
        height = kwargs.get('height', self.staging_folder.preview_height) or self.staging_folder.preview_height

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
        logger.debug('Page cache filename: %s', cache_filename)

        if storage_staging_file_image_cache.exists(cache_filename):
            logger.debug('Page cache file "%s" found', cache_filename)
            file_object = storage_staging_file_image_cache.open(cache_filename)
            converter = converter_class(file_object=file_object)

            converter.seek(0)
        else:
            logger.debug('Page cache file "%s" not found', cache_filename)
            try:
                file_object = open(self.get_full_path())
                converter = converter_class(file_object=file_object)

                page_image = converter.get_page()

                # Since open "wb+" doesn't create files, check if the file
                # exists, if not then create it
                if not storage_staging_file_image_cache.exists(cache_filename):
                    storage_staging_file_image_cache.save(name=cache_filename, content=ContentFile(content=''))

                with storage_staging_file_image_cache.open(cache_filename, 'wb+') as file_object:
                    file_object.write(page_image.getvalue())
            except Exception as exception:
                # Cleanup in case of error
                logger.error(
                    'Error creating page cache file "%s"; %s',
                    cache_filename, exception
                )
                storage_staging_file_image_cache.delete(cache_filename)
                if file_object:
                    file_object.close()
                raise

        for transformation in transformations:
            converter.transform(transformation=transformation)

        result = converter.get_page()
        file_object.close()
        return result
