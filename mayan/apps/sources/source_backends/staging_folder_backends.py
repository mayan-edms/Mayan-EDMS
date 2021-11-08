import base64
import logging
import os
from pathlib import Path
import time
from urllib.parse import quote_plus, unquote_plus

from furl import furl

from django import forms
from django.core.files import File
from django.core.files.base import ContentFile
from django.http import Http404, StreamingHttpResponse
from django.utils.encoding import force_text
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from rest_framework import status
from rest_framework.generics import get_object_or_404 as rest_get_object_or_404
from rest_framework.response import Response
from rest_framework.reverse import reverse as rest_framework_reverse

from mayan.apps.acls.models import AccessControlList
from mayan.apps.appearance.classes import Icon
from mayan.apps.common.menus import menu_object
from mayan.apps.converter.classes import ConverterBase
from mayan.apps.converter.exceptions import InvalidOfficeFormat
from mayan.apps.converter.transformations import TransformationResize
from mayan.apps.converter.utils import IndexedDictionary
from mayan.apps.documents.html_widgets import ThumbnailWidget
from mayan.apps.documents.models.document_type_models import DocumentType
from mayan.apps.documents.permissions import permission_document_create
from mayan.apps.navigation.classes import Link, SourceColumn
from mayan.apps.sources.classes import SourceBackend
from mayan.apps.sources.forms import UploadBaseForm
from mayan.apps.sources.literals import STORAGE_NAME_SOURCE_CACHE_FOLDER
from mayan.apps.sources.source_backends.mixins import (
    SourceBackendCompressedMixin, SourceBackendInteractiveMixin,
    SourceBaseMixin
)
from mayan.apps.storage.classes import DefinedStorage
from mayan.apps.storage.models import SharedUploadedFile

from ..classes import SourceBackendAction
from ..tasks import task_process_document_upload

__all__ = ('SourceBackendStagingFolder',)
logger = logging.getLogger(name=__name__)


class StagingFolderFile:
    """
    Simple class to extend the File class to add preview capabilities
    files in a directory on a storage.
    """
    def __init__(self, staging_folder, filename=None, encoded_filename=None):
        self.staging_folder = staging_folder
        if encoded_filename:
            self.encoded_filename = str(encoded_filename)

            try:
                self.filename = base64.urlsafe_b64decode(
                    unquote_plus(self.encoded_filename)
                ).decode('utf8')
            except UnicodeDecodeError:
                raise ValueError(
                    'Incorrect `encoded_filename` value.'
                )
        else:
            if not filename:
                raise KeyError(
                    'Supply either `encoded_filename` or `filename` when '
                    'instantiating a staging folder file.'
                )
            self.filename = filename
            self.encoded_filename = quote_plus(
                base64.urlsafe_b64encode(
                    filename.encode('utf8')
                )
            )

    def __str__(self):
        return force_text(s=self.filename)

    def as_file(self):
        return File(
            file=open(
                file=self.get_full_path(), mode='rb'
            ), name=self.filename
        )

    @property
    def cache_filename(self):
        return '{}-{}'.format(
            self.staging_folder.model_instance_id, self.encoded_filename
        )

    def delete(self):
        self.storage.delete(self.cache_filename)
        os.unlink(self.get_full_path())

    def generate_image(self, transformation_instance_list=None):
        # Check is transformed image is available.
        logger.debug('transformations cache filename: %s', self.cache_filename)

        if self.storage.exists(self.cache_filename):
            logger.debug(
                'staging file cache file "%s" found', self.cache_filename
            )
        else:
            logger.debug(
                'staging file cache file "%s" not found', self.cache_filename
            )
            image = self.get_image(
                transformation_instance_list=transformation_instance_list
            )

            # Since open "wb+" doesn't create files, check if the file
            # exists, if not then create it.
            self.storage.save(
                name=self.cache_filename, content=ContentFile(content='')
            )

            with self.storage.open(name=self.cache_filename, mode='wb+') as file_object:
                file_object.write(image.getvalue())

        return self.cache_filename

    def get_api_image_url(
        self, maximum_layer_order=None, transformation_instance_list=None,
        request=None, user=None
    ):
        final_url = furl()
        final_url.args = {'encoded_filename': self.encoded_filename}
        final_url.path = rest_framework_reverse(
            'rest_api:source-action', kwargs={
                'source_id': self.staging_folder.model_instance_id,
                'action_name': 'file_image'
            }, request=request
        )

        return final_url.tostr()

    def get_combined_transformation_list(
        self, maximum_layer_order=None, transformation_instance_list=None,
        user=None
    ):
        """
        Return a list of transformation containing the server side
        transformations for this object as well as transformations
        created from the arguments as transient interactive transformation.
        """
        result = [
            TransformationResize(
                width=self.staging_folder.kwargs['preview_width'],
                height=self.staging_folder.kwargs['preview_height'],
            )
        ]

        # Interactive transformations second.
        result.extend(transformation_instance_list or [])

        return result

    def get_date_time_created(self):
        return time.ctime(os.path.getctime(self.get_full_path()))

    def get_full_path(self):
        return os.path.join(
            self.staging_folder.kwargs['folder_path'], self.filename
        )

    def get_image(self, transformation_instance_list=None):
        try:
            with open(file=self.get_full_path(), mode='rb') as file_object:
                converter = ConverterBase.get_converter_class()(
                    file_object=file_object
                )

                try:
                    with converter.to_pdf() as pdf_file_object:
                        image_converter = ConverterBase.get_converter_class()(
                            file_object=pdf_file_object
                        )
                        page_image = image_converter.get_page()
                except InvalidOfficeFormat:
                    page_image = converter.get_page()
        except Exception as exception:
            # Cleanup in case of error.
            logger.error(
                'Error getting staging file image for file "%s"; %s',
                self.get_full_path(), exception
            )
            raise
        else:
            return page_image

    @cached_property
    def storage(self):
        return DefinedStorage.get(
            name=STORAGE_NAME_SOURCE_CACHE_FOLDER
        ).get_storage_instance()


class StagingUploadForm(UploadBaseForm):
    """
    Form that show all the files in the staging folder specified by the
    StagingFolderFile class passed as 'cls' argument.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            self.fields['staging_folder_file_id'].choices = [
                (
                    staging_folder_file.encoded_filename, force_text(s=staging_folder_file)
                ) for staging_folder_file in self.source.get_backend_instance().get_files()
            ]
        except Exception as exception:
            logger.error('exception: %s', exception)

    staging_folder_file_id = forms.ChoiceField(label=_('Staging file'))


class SourceBackendStagingFolder(
    SourceBackendCompressedMixin, SourceBackendInteractiveMixin,
    SourceBaseMixin, SourceBackend
):
    actions = (
        SourceBackendAction(
            name='file_delete', arguments=('encoded_filename',)
        ),
        SourceBackendAction(
            name='file_image', arguments=('encoded_filename',),
            confirmation=False
        ),
        SourceBackendAction(name='file_list', confirmation=False),
        SourceBackendAction(
            name='file_upload', arguments=(
                'document_type_id', 'encoded_filename', 'expand'
            )
        )
    )
    field_order = (
        'folder_path', 'preview_width', 'preview_height',
        'delete_after_upload'
    )
    fields = {
        'folder_path': {
            'class': 'django.forms.CharField',
            'default': '',
            'help_text': _(
                'Server side filesystem path.'
            ),
            'kwargs': {
                'max_length': 255,
            },
            'label': _('Folder path'),
            'required': True
        },
        'preview_width': {
            'class': 'django.forms.IntegerField',
            'help_text': _(
                'Width value to be passed to the converter backend.'
            ),
            'kwargs': {
                'min_value': 0
            },
            'label': _('Preview width'),
            'required': True
        },
        'preview_height': {
            'class': 'django.forms.IntegerField',
            'help_text': _(
                'Height value to be passed to the converter backend.'
            ),
            'kwargs': {
                'min_value': 0
            },
            'label': _('Preview height'),
            'required': False
        },
        'delete_after_upload': {
            'class': 'django.forms.BooleanField',
            'help_text': _(
                'Delete the file after is has been successfully uploaded.'
            ),
            'label': _('Delete after upload'),
            'required': False
        }
    }
    icon_staging_folder_file = Icon(driver_name='fontawesome', symbol='file')
    label = _('Staging folder')
    upload_form_class = StagingUploadForm

    @classmethod
    def intialize(cls):
        icon_staging_folder_file_delete = Icon(
            driver_name='fontawesome', symbol='times'
        )

        link_staging_folder_file_delete = Link(
            icon=icon_staging_folder_file_delete, kwargs={
                'source_id': 'source.pk',
                'action_name': '"file_delete"'
            }, permissions=(permission_document_create,), query={
                'document_id': 'document.pk',
                'document_type_id': 'document_type.pk',
                'source_id': 'source.pk',
                'encoded_filename': 'object.encoded_filename'
            }, tags='dangerous', text=_('Delete'),
            view='sources:source_action'
        )

        class StagingFolderFileThumbnailWidget(ThumbnailWidget):
            gallery_name = 'sources:staging_list'

            def disable_condition(self, instance):
                return True

        SourceColumn(
            func=lambda context: context['object'].get_date_time_created(),
            label=_('Created'), source=StagingFolderFile,
        )

        SourceColumn(
            label=_('Thumbnail'), source=StagingFolderFile,
            widget=StagingFolderFileThumbnailWidget,
            html_extra_classes='text-center'
        )

        menu_object.bind_links(
            links=(link_staging_folder_file_delete,), sources=(StagingFolderFile,)
        )

    def action_file_delete(self, request, encoded_filename):
        staging_folder_file = self.get_file(encoded_filename=encoded_filename)
        staging_folder_file.delete()

    def action_file_image(self, request, encoded_filename, **kwargs):
        # encoded_filename is passed as a list by the view's QueryDict
        encoded_filename = encoded_filename[0]

        query_dict = request.GET

        transformation_instance_list = IndexedDictionary(
            dictionary=query_dict
        ).as_instance_list()

        maximum_layer_order = request.GET.get('maximum_layer_order')
        if maximum_layer_order:
            maximum_layer_order = int(maximum_layer_order)

        staging_folder_file = self.get_file(encoded_filename=encoded_filename)

        combined_transformation_list = staging_folder_file.get_combined_transformation_list(
            maximum_layer_order=maximum_layer_order,
            transformation_instance_list=transformation_instance_list,
            user=request.user
        )

        cache_filename = staging_folder_file.generate_image(
            transformation_instance_list=combined_transformation_list
        )

        storage_staging_folder_file_image_cache = DefinedStorage.get(
            name=STORAGE_NAME_SOURCE_CACHE_FOLDER
        ).get_storage_instance()

        def file_generator():
            with storage_staging_folder_file_image_cache.open(name=cache_filename) as file_object:
                converter = ConverterBase.get_converter_class()(
                    file_object=file_object
                )
                for transformation in combined_transformation_list or ():
                    converter.transform(transformation=transformation)

                result = converter.get_page()

                while True:
                    chunk = result.read(File.DEFAULT_CHUNK_SIZE)
                    if not chunk:
                        break
                    else:
                        yield chunk

        response = StreamingHttpResponse(
            streaming_content=file_generator(), content_type='image'
        )
        return None, response

    def action_file_list(self, request):
        staging_folder_files = []

        for staging_folder_file in self.get_files():
            staging_folder_files.append(
                {
                    'filename': staging_folder_file.filename,
                    'delete-url': rest_framework_reverse(
                        viewname='rest_api:source-action', kwargs={
                            'source_id': staging_folder_file.staging_folder.model_instance_id,
                            'action_name': 'file_delete'
                        }, request=request
                    ),
                    'encoded_filename': staging_folder_file.encoded_filename,
                    'image-url': staging_folder_file.get_api_image_url(
                        request=request
                    ),
                    'upload-url': rest_framework_reverse(
                        viewname='rest_api:source-action', kwargs={
                            'source_id': staging_folder_file.staging_folder.model_instance_id,
                            'action_name': 'file_upload'
                        }, request=request
                    ),
                }
            )

        return staging_folder_files, None

    def action_file_upload(
        self, request, document_type_id, encoded_filename, expand=False
    ):
        staging_folder_file = self.get_file(encoded_filename=encoded_filename)

        queryset = AccessControlList.objects.restrict_queryset(
            queryset=DocumentType.objects.all(),
            permission=permission_document_create,
            user=request.user
        )

        document_type = rest_get_object_or_404(
            queryset=queryset, pk=document_type_id
        )

        self.process_kwargs = {
            'request': request,
            'staging_folder_file_filename': staging_folder_file.filename
        }

        shared_uploaded_file = SharedUploadedFile.objects.create(
            file=staging_folder_file.as_file()
        )

        kwargs = {
            'callback_kwargs': self.get_callback_kwargs(),
            'document_type_id': document_type.pk,
            'expand': expand,
            'shared_uploaded_file_id': shared_uploaded_file.pk,
            'source_id': self.model_instance_id,
            'user_id': request.user.pk
        }
        kwargs.update(self.get_task_extra_kwargs())

        task_process_document_upload.apply_async(kwargs=kwargs)

        return None, Response(status=status.HTTP_202_ACCEPTED)

    def callback(self, document_file, **kwargs):
        if self.kwargs.get('delete_after_upload'):
            path = Path(
                self.kwargs['folder_path'], kwargs['staging_folder_file_filename']
            )

            try:
                path.unlink()
            except Exception as exception:
                logger.error(
                    'Error deleting staging file: %s; %s',
                    path, exception
                )
                raise Exception(
                    _('Error deleting staging file; %s') % exception
                )

    def get_callback_kwargs(self):
        callback_kwargs = super().get_callback_kwargs()

        callback_kwargs.update(
            {
                'staging_folder_file_filename': self.process_kwargs['staging_folder_file_filename']
            }
        )

        return callback_kwargs

    def get_action_file_delete_context(self, view, encoded_filename):
        staging_folder_file = self.get_file(encoded_filename=encoded_filename)

        context = {
            'delete_view': True,
            'object': staging_folder_file,
            'object_name': _('Staging file'),
            'title': _('Delete staging file "%s"?') % staging_folder_file,
        }

        view_kwargs = view.get_all_kwargs()

        if 'document_type_id' in view_kwargs:
            context['document_type'] = DocumentType.objects.get(pk=view_kwargs['document_type_id'][0])

        return context

    def get_file(self, *args, **kwargs):
        try:
            return StagingFolderFile(staging_folder=self, *args, **kwargs)
        except (KeyError, ValueError):
            raise Http404

    def get_files(self):
        try:
            for entry in sorted([os.path.normcase(f) for f in os.listdir(self.kwargs['folder_path']) if os.path.isfile(os.path.join(self.kwargs['folder_path'], f))]):
                yield self.get_file(filename=entry)
        except OSError as exception:
            logger.error(
                'Unable get list of staging files from source: %s; %s',
                self, exception
            )
            raise Exception(
                _('Unable get list of staging files: %s') % exception
            )

    def get_shared_uploaded_files(self):
        staging_folder_file = self.get_file(
            encoded_filename=self.process_kwargs['forms']['source_form'].cleaned_data['staging_folder_file_id']
        )
        self.process_kwargs['staging_folder_file_filename'] = staging_folder_file.filename

        return (
            SharedUploadedFile.objects.create(file=staging_folder_file.as_file()),
        )

    def get_view_context(self, context, request):
        subtemplates_list = [
            {
                'name': 'appearance/generic_multiform_subtemplate.html',
                'context': {
                    'forms': context['forms'],
                },
            },
            {
                'name': 'appearance/generic_list_subtemplate.html',
                'context': {
                    'hide_link': True,
                    'no_results_icon': SourceBackendStagingFolder.icon_staging_folder_file,
                    'no_results_text': _(
                        'This could mean that the staging folder is '
                        'empty. It could also mean that the '
                        'operating system user account being used '
                        'for Mayan EDMS doesn\'t have the necessary '
                        'file system permissions for the folder.'
                    ),
                    'no_results_title': _(
                        'No staging files available'
                    ),
                    'object_list': list(self.get_files()),
                }
            },
        ]

        return {
            'subtemplates_list': subtemplates_list
        }
