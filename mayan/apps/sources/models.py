from __future__ import absolute_import

from ast import literal_eval
import logging
import os

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _

from model_utils.managers import InheritanceManager

from acls.utils import apply_default_acls
from common.compressed_files import CompressedFile, NotACompressedFile
from converter.api import get_available_transformations_choices
from converter.literals import DIMENSION_SEPARATOR
from documents.events import HISTORY_DOCUMENT_CREATED
from documents.models import Document
from history.api import create_history
from metadata.api import save_metadata_list

from .classes import StagingFile
from .literals import (SOURCE_CHOICES, SOURCE_CHOICES_PLURAL,
                       SOURCE_CHOICE_STAGING, SOURCE_CHOICE_WATCH,
                       SOURCE_CHOICE_WEB_FORM,
                       SOURCE_INTERACTIVE_UNCOMPRESS_CHOICES,
                       SOURCE_UNCOMPRESS_CHOICES)
from .managers import SourceTransformationManager

logger = logging.getLogger(__name__)


class Source(models.Model):
    title = models.CharField(max_length=64, verbose_name=_(u'Title'))
    enabled = models.BooleanField(default=True, verbose_name=_(u'Enabled'))
    whitelist = models.TextField(blank=True, verbose_name=_(u'Whitelist'), editable=False)
    blacklist = models.TextField(blank=True, verbose_name=_(u'Blacklist'), editable=False)

    objects = InheritanceManager()

    @classmethod
    def class_fullname(cls):
        return unicode(dict(SOURCE_CHOICES).get(cls.source_type))

    @classmethod
    def class_fullname_plural(cls):
        return unicode(dict(SOURCE_CHOICES_PLURAL).get(cls.source_type))

    def __unicode__(self):
        return u'%s' % self.title

    def fullname(self):
        return u' '.join([self.class_fullname(), '"%s"' % self.title])

    def internal_name(self):
        return u'%s_%d' % (self.source_type, self.pk)

    def get_transformation_list(self):
        return SourceTransformation.transformations.get_for_object_as_list(self)

    def upload_file(self, file_object, filename=None, use_file_name=False, document_type=None, expand=False, metadata_dict_list=None, user=None, document=None, new_version_data=None, command_line=False, description=None):
        is_compressed = None

        if expand:
            try:
                cf = CompressedFile(file_object)
                count = 1
                for fp in cf.children():
                    if command_line:
                        print 'Uploading file #%d: %s' % (count, fp)
                    self.upload_single_file(file_object=fp, filename=None, document_type=document_type, metadata_dict_list=metadata_dict_list, user=user, description=description)
                    fp.close()
                    count += 1

            except NotACompressedFile:
                is_compressed = False
                logging.debug('Exception: NotACompressedFile')
                if command_line:
                    raise
                self.upload_single_file(file_object=file_object, filename=filename, document_type=document_type, metadata_dict_list=metadata_dict_list, user=user, description=description)
            else:
                is_compressed = True
        else:
            self.upload_single_file(file_object, filename, use_file_name, document_type, metadata_dict_list, user, document, new_version_data, description=description)

        file_object.close()
        return {'is_compressed': is_compressed}

    @transaction.atomic
    def upload_single_file(self, file_object, filename=None, use_file_name=False, document_type=None, metadata_dict_list=None, user=None, document=None, new_version_data=None, description=None):
        new_document = not document

        if not document:
            document = Document()
            if document_type:
                document.document_type = document_type

            if description:
                document.description = description

            document.save()

            # TODO: move this to the Document model
            apply_default_acls(document, user)

            # TODO: move this to the Document model
            if user:
                document.add_as_recent_document_for_user(user)
                create_history(HISTORY_DOCUMENT_CREATED, document, {'user': user})
            else:
                create_history(HISTORY_DOCUMENT_CREATED, document)
        else:
            if use_file_name:
                filename = None
            else:
                filename = filename if filename else document.latest_version.filename

            if description:
                document.description = description
                document.save()

        if not new_version_data:
            new_version_data = {}

        new_version = document.new_version(file=file_object, user=user, **new_version_data)

        if filename:
            document.rename(filename)

        transformations, errors = self.get_transformation_list()

        new_version.apply_default_transformations(transformations)
        # TODO: new HISTORY for version updates

        if metadata_dict_list and new_document:
            # Only do for new documents
            save_metadata_list(metadata_dict_list, document, create=True)

    class Meta:
        ordering = ('title',)
        verbose_name = _(u'Source')
        verbose_name_plural = _(u'Sources')


class InteractiveSource(Source):
    class Meta:
        verbose_name = _(u'Interactive source')
        verbose_name_plural = _(u'Interactive sources')


class StagingFolderSource(InteractiveSource):
    is_interactive = True
    source_type = SOURCE_CHOICE_STAGING

    folder_path = models.CharField(max_length=255, verbose_name=_(u'Folder path'), help_text=_(u'Server side filesystem path.'))
    preview_width = models.IntegerField(verbose_name=_(u'Preview width'), help_text=_(u'Width value to be passed to the converter backend.'))
    preview_height = models.IntegerField(blank=True, null=True, verbose_name=_(u'Preview height'), help_text=_(u'Height value to be passed to the converter backend.'))
    uncompress = models.CharField(max_length=1, choices=SOURCE_INTERACTIVE_UNCOMPRESS_CHOICES, verbose_name=_(u'Uncompress'), help_text=_(u'Whether to expand or not compressed archives.'))
    delete_after_upload = models.BooleanField(default=True, verbose_name=_(u'Delete after upload'), help_text=_(u'Delete the file after is has been successfully uploaded.'))

    def get_preview_size(self):
        dimensions = []
        dimensions.append(unicode(self.preview_width))
        if self.preview_height:
            dimensions.append(unicode(self.preview_height))

        return DIMENSION_SEPARATOR.join(dimensions)

    def get_file(self, *args, **kwargs):
        return StagingFile(staging_folder=self, *args, **kwargs)

    def get_files(self):
        try:
            for entry in sorted([os.path.normcase(f) for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))]):
                yield self.get_file(filename=entry)
        except OSError as exception:
            raise Exception(_(u'Unable get list of staging files: %s') % exception)

    class Meta:
        verbose_name = _(u'Staging folder')
        verbose_name_plural = _(u'Staging folders')


class WebFormSource(InteractiveSource):
    is_interactive = True
    source_type = SOURCE_CHOICE_WEB_FORM

    uncompress = models.CharField(max_length=1, choices=SOURCE_INTERACTIVE_UNCOMPRESS_CHOICES, verbose_name=_(u'Uncompress'), help_text=_(u'Whether to expand or not compressed archives.'))
    # Default path

    class Meta:
        verbose_name = _(u'Web form')
        verbose_name_plural = _(u'Web forms')


class OutOfProcessSource(Source):
    is_interactive = False

    class Meta:
        verbose_name = _(u'Out of process')
        verbose_name_plural = _(u'Out of process')


class WatchFolderSource(OutOfProcessSource):
    is_interactive = False
    source_type = SOURCE_CHOICE_WATCH

    folder_path = models.CharField(max_length=255, verbose_name=_(u'Folder path'), help_text=_(u'Server side filesystem path.'))
    uncompress = models.CharField(max_length=1, choices=SOURCE_UNCOMPRESS_CHOICES, verbose_name=_(u'Uncompress'), help_text=_(u'Whether to expand or not compressed archives.'))
    delete_after_upload = models.BooleanField(default=True, verbose_name=_(u'Delete after upload'), help_text=_(u'Delete the file after is has been successfully uploaded.'))
    interval = models.PositiveIntegerField(verbose_name=_(u'Interval'), help_text=_(u'Inverval in seconds where the watch folder path is checked for new documents.'))

    class Meta:
        verbose_name = _(u'Watch folder')
        verbose_name_plural = _(u'Watch folders')


class ArgumentsValidator(object):
    message = _(u'Enter a valid value.')
    code = 'invalid'

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        """
        Validates that the input evaluates correctly.
        """
        value = value.strip()
        try:
            literal_eval(value)
        except (ValueError, SyntaxError):
            raise ValidationError(self.message, code=self.code)


class SourceTransformation(models.Model):
    """
    Model that stores the transformation and transformation arguments
    for a given document source
    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    order = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name=_(u'Order'), db_index=True)
    transformation = models.CharField(choices=get_available_transformations_choices(), max_length=128, verbose_name=_(u'Transformation'))
    arguments = models.TextField(blank=True, null=True, verbose_name=_(u'Arguments'), help_text=_(u'Use dictionaries to indentify arguments, example: %s') % u'{\'degrees\':90}', validators=[ArgumentsValidator()])

    objects = models.Manager()
    transformations = SourceTransformationManager()

    def __unicode__(self):
        return self.get_transformation_display()

    class Meta:
        ordering = ('order',)
        verbose_name = _(u'Document source transformation')
        verbose_name_plural = _(u'Document source transformations')
