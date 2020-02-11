from __future__ import unicode_literals

import copy
from io import BytesIO
import logging
import os
import shutil

import PIL
from PIL import Image
import sh

from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from mayan.apps.appearance.classes import Icon
from mayan.apps.mimetype.api import get_mimetype
from mayan.apps.navigation.classes import Link
from mayan.apps.storage.settings import setting_temporary_directory
from mayan.apps.storage.utils import (
    NamedTemporaryFile, fs_cleanup, mkdtemp
)

from .exceptions import InvalidOfficeFormat, OfficeConversionError
from .literals import (
    CONVERTER_OFFICE_FILE_MIMETYPES, DEFAULT_LIBREOFFICE_PATH,
    DEFAULT_PAGE_NUMBER, DEFAULT_PILLOW_FORMAT
)
from .settings import setting_graphics_backend_arguments

libreoffice_path = setting_graphics_backend_arguments.value.get(
    'libreoffice_path', DEFAULT_LIBREOFFICE_PATH
)

logger = logging.getLogger(__name__)


class ConverterBase(object):
    def __init__(self, file_object, mime_type=None):
        self.file_object = file_object
        self.image = None
        self.mime_type = mime_type or get_mimetype(
            file_object=file_object, mimetype_only=False
        )[0]
        self.soffice_file = None
        Image.init()
        try:
            self.command_libreoffice = sh.Command(libreoffice_path).bake(
                '--headless', '--convert-to', 'pdf:writer_pdf_Export'
            )
        except sh.CommandNotFound:
            self.command_libreoffice = None

    def convert(self, page_number=DEFAULT_PAGE_NUMBER):
        self.page_number = page_number

    def detect_orientation(self, page_number):
        # Must be overridden by subclass
        pass

    def get_page(self, output_format=None):
        output_format = output_format or setting_graphics_backend_arguments.value.get(
            'pillow_format', DEFAULT_PILLOW_FORMAT
        )

        if not self.image:
            self.seek_page(page_number=0)

        image_buffer = BytesIO()
        new_mode = self.image.mode

        if output_format.upper() == 'JPEG':
            # JPEG doesn't support transparency channel, convert the image to
            # RGB. Removes modes: P and RGBA
            new_mode = 'RGB'

        self.image.convert(new_mode).save(image_buffer, format=output_format)

        image_buffer.seek(0)

        return image_buffer

    def get_page_count(self):
        try:
            self.soffice_file = self.to_pdf()
        except InvalidOfficeFormat as exception:
            logger.debug('Is not an office format document; %s', exception)

    def seek_page(self, page_number):
        """
        Seek the specified page number from the source file object.
        If the file is a paged image get the page if not convert it to a
        paged image format and return the specified page as an image.
        """
        # Starting with #0
        self.file_object.seek(0)

        try:
            self.image = Image.open(self.file_object)
        except IOError:
            # Cannot identify image file
            self.image = self.convert(page_number=page_number)
        except PIL.Image.DecompressionBombError as exception:
            logger.error(
                'Unable to seek document page. Increase the value of '
                'the argument "pillow_maximum_image_pixels" in the '
                'CONVERTER_GRAPHICS_BACKEND_ARGUMENTS setting; %s',
                exception
            )
            raise
        else:
            self.image.seek(page_number)
            self.image.load()

    def soffice(self):
        """
        Executes LibreOffice as a sub process
        """
        if not self.command_libreoffice:
            raise OfficeConversionError(
                _('LibreOffice not installed or not found.')
            )

        with NamedTemporaryFile() as temporary_file_object:
            # Copy the source file object of the converter instance to a
            # named temporary file to be able to pass it to the LibreOffice
            # execution.
            self.file_object.seek(0)
            shutil.copyfileobj(
                fsrc=self.file_object, fdst=temporary_file_object
            )
            self.file_object.seek(0)
            temporary_file_object.seek(0)

            libreoffice_home_directory = mkdtemp()
            args = (
                temporary_file_object.name, '--outdir', setting_temporary_directory.value,
                '-env:UserInstallation=file://{}'.format(
                    os.path.join(
                        libreoffice_home_directory, 'LibreOffice_Conversion'
                    )
                ),
            )

            kwargs = {'_env': {'HOME': libreoffice_home_directory}}

            if self.mime_type == 'text/plain':
                kwargs.update(
                    {'infilter': 'Text (encoded):UTF8,LF,,,'}
                )

            try:
                self.command_libreoffice(*args, **kwargs)
            except sh.ErrorReturnCode as exception:
                temporary_file_object.close()
                raise OfficeConversionError(exception)
            except Exception as exception:
                temporary_file_object.close()
                logger.error('Exception launching Libre Office; %s', exception)
                raise
            finally:
                fs_cleanup(filename=libreoffice_home_directory)

            # LibreOffice return a PDF file with the same name as the input
            # provided but with the .pdf extension.

            # Get the converted output file path out of the temporary file
            # name plus the temporary directory

            filename, extension = os.path.splitext(
                os.path.basename(temporary_file_object.name)
            )

            logger.debug('filename: %s', filename)
            logger.debug('extension: %s', extension)

            converted_file_path = os.path.join(
                setting_temporary_directory.value, os.path.extsep.join(
                    (filename, 'pdf')
                )
            )
            logger.debug('converted_file_path: %s', converted_file_path)

        # Don't use context manager with the NamedTemporaryFile on purpose
        # so that it is deleted when the caller closes the file and not
        # before.

        temporary_converted_file_object = NamedTemporaryFile()

        # Copy the LibreOffice output file to a new named temporary file
        # and delete the converted file
        with open(converted_file_path, mode='rb') as converted_file_object:
            shutil.copyfileobj(
                fsrc=converted_file_object, fdst=temporary_converted_file_object
            )
        fs_cleanup(filename=converted_file_path)
        temporary_converted_file_object.seek(0)
        return temporary_converted_file_object

    def to_pdf(self):
        if self.mime_type in CONVERTER_OFFICE_FILE_MIMETYPES:
            return self.soffice()
        else:
            raise InvalidOfficeFormat(_('Not an office file format.'))

    def transform(self, transformation):
        if not self.image:
            self.seek_page(page_number=0)

        self.image = transformation.execute_on(image=self.image)

    def transform_many(self, transformations):
        if not self.image:
            self.seek_page(page_number=0)

        for transformation in transformations:
            self.image = transformation.execute_on(image=self.image)


@python_2_unicode_compatible
class Layer(object):
    _registry = {}

    @classmethod
    def all(cls):
        return cls._registry.values()

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def get_by_value(cls, key, value):
        for name, layer in cls._registry.items():
            if getattr(layer, key) == value:
                return layer

    @classmethod
    def invalidate_cache(cls):
        for layer in cls.all():
            layer.__dict__.pop('stored_layer', None)

    @classmethod
    def update(cls):
        for layer in cls.all():
            layer.stored_layer

    def __init__(
        self, label, name, order, permissions, default=False,
        empty_results_text=None, symbol=None,
    ):
        """
        access_permission is the permission necessary to view the layer.
        exclude_permission is the permission necessary to discard the layer.
        """
        self.default = default
        self.empty_results_text = empty_results_text
        self.label = label
        self.name = name
        self.order = order
        self.permissions = permissions
        self.symbol = symbol

        # Check order
        layer = self.__class__.get_by_value(key='order', value=self.order)

        if layer:
            raise ImproperlyConfigured(
                'Layer "{}" already has order "{}" requested by layer "{}"'.format(
                    layer.name, order, self.name
                )
            )

        # Check default
        if default:
            layer = self.__class__.get_by_value(key='default', value=True)
            if layer:
                raise ImproperlyConfigured(
                    'Layer "{}" is already the default layer; "{}"'.format(
                        layer.name, self.name
                    )
                )

        self.__class__._registry[name] = self

    def get_permission(self, name):
        return self.permissions.get(name, None)

    def __str__(self):
        return force_text(self.label)

    def add_transformation_to(self, obj, transformation_class, arguments=None):
        ContentType = apps.get_model(
            app_label='contenttypes', model_name='ContentType'
        )
        content_type = ContentType.objects.get_for_model(model=obj)
        object_layer, created = self.stored_layer.object_layers.get_or_create(
            content_type=content_type, object_id=obj.pk
        )
        object_layer.transformations.create(
            name=transformation_class.name, arguments=arguments
        )

    def copy_transformations(self, source, targets):
        """
        Copy transformation from source to all targets
        """
        ContentType = apps.get_model(
            app_label='contenttypes', model_name='ContentType'
        )

        transformations = self.get_transformations_for(obj=source)

        with transaction.atomic():
            for target in targets:
                content_type = ContentType.objects.get_for_model(model=target)
                object_layer, created = self.stored_layer.object_layers.get_or_create(
                    content_type=content_type, object_id=target.pk
                )
                for transformation in transformations:
                    object_layer.transformations.create(
                        order=transformation.order,
                        name=transformation.name,
                        arguments=transformation.arguments,
                    )

    def get_empty_results_text(self):
        if self.empty_results_text:
            return self.empty_results_text
        else:
            return _(
                'Transformations allow changing the visual appearance '
                'of documents without making permanent changes to the '
                'document file themselves.'
            )

    def get_icon(self):
        return Icon(driver_name='fontawesome', symbol=self.symbol)

    def get_model_instance(self):
        StoredLayer = apps.get_model(
            app_label='converter', model_name='StoredLayer'
        )
        stored_layer, created = StoredLayer.objects.update_or_create(
            name=self.name, defaults={'order': self.order}
        )

        return stored_layer

    def get_transformations_for(self, obj, as_classes=False):
        """
        as_classes == True returns the transformation classes from .classes
        ready to be feed to the converter class
        """
        LayerTransformation = apps.get_model(
            app_label='converter', model_name='LayerTransformation'
        )

        return LayerTransformation.objects.get_for_object(
            obj=obj, as_classes=as_classes,
            only_stored_layer=self.stored_layer
        )

    @cached_property
    def stored_layer(self):
        return self.get_model_instance()


class LayerLink(Link):
    @staticmethod
    def set_icon(instance, layer):
        if instance.action == 'list':
            if layer.symbol:
                instance.icon_class = layer.get_icon()

    def __init__(self, action, layer, object_name=None, **kwargs):
        super(LayerLink, self).__init__(**kwargs)
        self.action = action
        self.layer = layer
        self.object_name = object_name or _('transformation')

        permission = layer.permissions.get(action, None)
        if permission:
            self.permissions = (permission,)

        if action == 'list':
            self.kwargs = LayerLinkKwargsFactory(
                layer_name=layer.name
            ).get_kwargs_function()

        if action in ('create', 'select'):
            self.kwargs = LayerLinkKwargsFactory().get_kwargs_function()

        LayerLink.set_icon(instance=self, layer=layer)

    def copy(self, layer):
        result = copy.copy(self)
        result.kwargs = LayerLinkKwargsFactory(
            layer_name=layer.name
        ).get_kwargs_function()
        result._layer_name = layer.name

        LayerLink.set_icon(instance=result, layer=layer)

        return result

    @cached_property
    def layer_name(self):
        return getattr(
            self, '_layer_name', Layer.get_by_value(
                key='default', value=True
            ).name
        )


class LayerLinkKwargsFactory(object):
    def __init__(self, layer_name=None, variable_name='resolved_object'):
        self.layer_name = layer_name
        self.variable_name = variable_name

    def get_kwargs_function(self):
        def get_kwargs(context):
            ContentType = apps.get_model(
                app_label='contenttypes', model_name='ContentType'
            )

            content_type = ContentType.objects.get_for_model(
                context[self.variable_name]
            )
            default_layer = Layer.get_by_value(key='default', value=True)
            return {
                'app_label': '"{}"'.format(content_type.app_label),
                'model': '"{}"'.format(content_type.model),
                'object_id': '{}.pk'.format(self.variable_name),
                'layer_name': '"{}"'.format(
                    self.layer_name or context.get(
                        'layer_name', default_layer.name
                    )
                )
            }

        return get_kwargs
