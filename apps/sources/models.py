from __future__ import absolute_import

from ast import literal_eval
import logging
import poplib
import imaplib
from email.Utils import collapse_rfc2231_value
from email import message_from_string
import os
import datetime

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import imagescanner

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.exceptions import ValidationError
from django.db import transaction
from django.core.files import File

#from converter.api import get_available_transformations_choices
from converter.literals import DIMENSION_SEPARATOR
from documents.models import Document, DocumentType
from documents.events import history_document_created
from metadata.api import save_metadata_list
from acls.utils import apply_default_acls

from .managers import SourceTransformationManager, SourceLogManager
from .literals import (SOURCE_CHOICES, SOURCE_CHOICES_PLURAL,
    SOURCE_INTERACTIVE_UNCOMPRESS_CHOICES, SOURCE_CHOICE_WEB_FORM,
    SOURCE_CHOICE_STAGING, DISK, DRIVE,
    SOURCE_ICON_CHOICES, SOURCE_CHOICE_WATCH, SOURCE_UNCOMPRESS_CHOICES,
    SOURCE_UNCOMPRESS_CHOICE_Y,
    POP3_PORT, POP3_SSL_PORT,
    SOURCE_CHOICE_POP3_EMAIL, DEFAULT_POP3_INTERVAL,
    IMAP_PORT, IMAP_SSL_PORT,
    SOURCE_CHOICE_IMAP_EMAIL, DEFAULT_IMAP_INTERVAL,
    IMAP_DEFAULT_MAILBOX,
    SOURCE_CHOICE_LOCAL_SCANNER, IMAGES,
    DEFAULT_LOCAL_SCANNER_FILE_FORMAT)
from .compressed_file import CompressedFile, NotACompressedFile
#from .post_init import sources_scheduler

logger = logging.getLogger(__name__)


class BaseModel(models.Model):
    title = models.CharField(max_length=64, verbose_name=_(u'title'))
    enabled = models.BooleanField(default=True, verbose_name=_(u'enabled'))
    whitelist = models.TextField(blank=True, verbose_name=_(u'whitelist'), editable=False)
    blacklist = models.TextField(blank=True, verbose_name=_(u'blacklist'), editable=False)
    #document_type = models.ForeignKey(DocumentType, blank=True, null=True, verbose_name=_(u'document type'), help_text=(u'Optional document type to be applied to documents uploaded from this source.'))

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

    def upload_file(self, file_object, filename=None, use_file_name=False, document_type=None, expand=False, metadata_dict_list=None, user=None, document=None, new_version_data=None, command_line=False):
        is_compressed = None

        if expand:
            try:
                cf = CompressedFile(file_object)
                count = 1
                for fp in cf.children():
                    if command_line:
                        print 'Uploading file #%d: %s' % (count, fp)
                    self.upload_single_file(file_object=fp, filename=None, document_type=document_type, metadata_dict_list=metadata_dict_list, user=user)
                    fp.close()
                    count += 1

            except NotACompressedFile:
                is_compressed = False
                logging.debug('Exception: NotACompressedFile')
                if command_line:
                    raise
                self.upload_single_file(file_object=file_object, filename=filename, document_type=document_type, metadata_dict_list=metadata_dict_list, user=user)
            else:
                is_compressed = True
        else:
            self.upload_single_file(file_object, filename, use_file_name, document_type, metadata_dict_list, user, document, new_version_data)

        file_object.close()
        return {'is_compressed': is_compressed}

    @transaction.commit_on_success
    def upload_single_file(self, file_object, filename=None, use_file_name=False, document_type=None, metadata_dict_list=None, user=None, document=None, new_version_data=None):
        new_document = not document

        if not document:
            document = Document()
            if document_type:
                document.document_type = document_type
            document.save()

            apply_default_acls(document, user)

            if user:
                document.add_as_recent_document_for_user(user)
                history_document_created.commit(source_object=document, data={'user': user})
            else:
                history_document_created.commit(source_object=document)
        else:
            if use_file_name:
                filename = None
            else:
                filename = filename if filename else document.latest_version.filename

        if not new_version_data:
            new_version_data = {}

        try:
            new_version = document.new_version(file=file_object, user=user, **new_version_data)
        except Exception, exc:
            logger.error('Unhandled exception: %s' % exc)
            # Don't leave the database in a broken state
            # Delete invalid documents with no version child
            # For databases that doesn't support transactions, delete the document
            if document.version_set.count() == 0:
                logger.debug('Empty document with no previous versions, deleting.')
                document.delete()
            # Rollback everything in case the database DOES support
            # transactions
            transaction.rollback()
            # Re-raise the error so that the view can capture
            # and display it
            raise

        if filename:
            document.rename(filename)

        transformations, errors = self.get_transformation_list()

        new_version.apply_default_transformations(transformations)
        #TODO: new HISTORY for version updates

        if metadata_dict_list and new_document:
            # Only do for new documents
            save_metadata_list(metadata_dict_list, document, create=True)

    class Meta:
        ordering = ('title',)
        abstract = True


class SourceLog(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    source = generic.GenericForeignKey('content_type', 'object_id')
    creation_datetime = models.DateTimeField(verbose_name=_(u'date time'))
    status = models.TextField(verbose_name=_(u'status'))

    objects = SourceLogManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.creation_datetime = datetime.datetime.now()
        return super(SourceLog, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _(u'source log')
        verbose_name_plural = _(u'sources logs')
        get_latest_by = 'creation_datetime'
        ordering = ('creation_datetime',)


class InteractiveBaseModel(BaseModel):
    icon = models.CharField(blank=True, null=True, max_length=24, choices=SOURCE_ICON_CHOICES, verbose_name=_(u'icon'), help_text=_(u'An icon to visually distinguish this source.'))

    def save(self, *args, **kwargs):
        if not self.icon:
            self.icon = self.default_icon
        super(BaseModel, self).save(*args, **kwargs)

    class Meta(BaseModel.Meta):
        abstract = True


class PseudoFile(File):
    def __init__(self, file, name):
        self.name = name
        self.file = file
        self.file.seek(0, os.SEEK_END)
        self.size = self.file.tell()
        self.file.seek(0)


class Attachment(File):
    def __init__(self, part, name):
        self.name = name
        self.file = PseudoFile(StringIO(part.get_payload(decode=True)), name=name)


class IntervalBaseModel(BaseModel):
    is_interactive = False   

    interval = models.PositiveIntegerField(default=DEFAULT_POP3_INTERVAL, verbose_name=_(u'interval'), help_text=_(u'Interval in seconds between document downloads from this source.'))
    document_type = models.ForeignKey(DocumentType, null=True, blank=True, verbose_name=_(u'document type'), help_text=_(u'Assign a document type to documents uploaded from this source.'))
    uncompress = models.CharField(max_length=1, choices=SOURCE_UNCOMPRESS_CHOICES, verbose_name=_(u'uncompress'), help_text=_(u'Whether to expand or not, compressed archives.'))

    class Meta(BaseModel.Meta):
        verbose_name = _(u'interval source')
        verbose_name_plural = _(u'interval sources')
        abstract = True


class EmailBaseModel(IntervalBaseModel):
    host = models.CharField(max_length=64, verbose_name=_(u'host'))
    ssl = models.BooleanField(verbose_name=_(u'SSL'))
    port = models.PositiveIntegerField(blank=True, null=True, verbose_name=_(u'port'), help_text=_(u'Override the defaults values of %(normal_port)d and %(ssl_port)d for SSL, can be left blank otherwise.') % {'normal_port': POP3_PORT, 'ssl_port': POP3_SSL_PORT})
    username = models.CharField(max_length=64, verbose_name=_(u'username'))
    password = models.CharField(max_length=64, verbose_name=_(u'password'))

    # From: http://bookmarks.honewatson.com/2009/08/11/python-gmail-imaplib-search-subject-get-attachments/
    @staticmethod
    def process_message(source, message):
        email = message_from_string(message)
        counter = 1

        for part in email.walk():
            disposition = part.get('Content-Disposition', 'none')
            logger.debug('Disposition: %s' % disposition)

            if disposition.startswith('attachment'):
                raw_filename = part.get_filename()

                if raw_filename:
                    filename = collapse_rfc2231_value(raw_filename)
                else:
                    filename = _(u'attachment-%i') % counter
                    counter += 1

                logger.debug('filename: %s' % filename)

                document_file = Attachment(part, name=filename)
                source.upload_file(document_file, expand=(source.uncompress == SOURCE_UNCOMPRESS_CHOICE_Y), document_type=source.document_type)

    class Meta(IntervalBaseModel.Meta):
        verbose_name = _(u'email source')
        verbose_name_plural = _(u'email sources')
        abstract = True


class POP3Email(EmailBaseModel):
    source_type = SOURCE_CHOICE_POP3_EMAIL

    def fetch_mail(self):
        from .settings import POP3_TIMEOUT

        try:
            last_check = SourceLog.objects.get_latest_for(self)
        except SourceLog.DoesNotExist:
            # Trigger email fetch when there are no previous logs
            initial_trigger = True
            difference = datetime.timedelta(seconds=0)
        else:
            difference = datetime.datetime.now() - last_check
            initial_trigger = False

        if difference >= datetime.timedelta(seconds=self.interval) or initial_trigger:
            try:
                logger.debug('Starting POP3 email fetch')
                logger.debug('host: %s' % self.host)
                logger.debug('ssl: %s' % self.ssl)
                if self.ssl:
                    port = self.port or POP3_SSL_PORT
                    logger.debug('port: %d' % port)
                    mailbox = poplib.POP3_SSL(self.host, int(port))
                else:
                    port = self.port or POP3_PORT
                    logger.debug('port: %d' % port)
                    mailbox = poplib.POP3(self.host, int(port), timeout=POP3_TIMEOUT) 

                mailbox.getwelcome()
                mailbox.user(self.username)
                mailbox.pass_(self.password)
                messages_info = mailbox.list()

                logger.debug('messages_info:')
                logger.debug(messages_info)
                logger.debug('messages count: %s' % len(messages_info[1]))

                for message_info in messages_info[1]:
                    message_number, message_size = message_info.split()
                    logger.debug('message_number: %s' % message_number)
                    logger.debug('message_size: %s' % message_size)

                    complete_message = '\n'.join(mailbox.retr(message_number)[1])

                    EmailBaseModel.process_message(source=self, message=complete_message)
                    mailbox.dele(message_number)

                mailbox.quit()
                SourceLog.objects.save_status(source=self, status='Successful connection.')

            except Exception, exc:
                logger.error('Unhandled exception: %s' % exc)
                SourceLog.objects.save_status(source=self, status='Error: %s' % exc)

    class Meta(EmailBaseModel.Meta):
        verbose_name = _(u'POP email')
        verbose_name_plural = _(u'POP email')


class IMAPEmail(EmailBaseModel):
    source_type = SOURCE_CHOICE_IMAP_EMAIL

    mailbox = models.CharField(max_length=64, blank=True, verbose_name=_(u'mailbox'), help_text=_(u'Mail from which to check for messages with attached documents.  If none is specified, the default mailbox is %s') % IMAP_DEFAULT_MAILBOX)

    # http://www.doughellmann.com/PyMOTW/imaplib/
    def fetch_mail(self):
        try:
            last_check = SourceLog.objects.get_latest_for(self)
        except SourceLog.DoesNotExist:
            # Trigger email fetch when there are no previous logs
            initial_trigger = True
            difference = datetime.timedelta(seconds=0)
        else:
            difference = datetime.datetime.now() - last_check
            initial_trigger = False

        if difference >= datetime.timedelta(seconds=self.interval) or initial_trigger:
            try:
                logger.debug('Starting IMAP email fetch')
                logger.debug('host: %s' % self.host)
                logger.debug('ssl: %s' % self.ssl)
                if self.ssl:
                    port = self.port or IMAP_SSL_PORT
                    logger.debug('port: %d' % port)
                    mailbox = imaplib.IMAP4_SSL(self.host, int(port))
                else:
                    port = self.port or IMAP_PORT
                    logger.debug('port: %d' % port)
                    mailbox = imaplib.IMAP4(self.host, int(port))

                mailbox.login(self.username, self.password)
                mailbox.select(self.mailbox or IMAP_DEFAULT_MAILBOX)

                status, data = mailbox.search(None, 'NOT', 'DELETED')
                if data:
                    messages_info = data[0].split()
                    logger.debug('messages count: %s' % len(messages_info))

                    for message_number in messages_info:
                        logger.debug('message_number: %s' % message_number)
                        status, data = mailbox.fetch(message_number, '(RFC822)')
                        EmailBaseModel.process_message(source=self, message=data[0][1])
                        mailbox.store(message_number, '+FLAGS', '\\Deleted')

                mailbox.expunge()
                mailbox.close()
                mailbox.logout()
                SourceLog.objects.save_status(source=self, status='Successful connection.')

            except Exception, exc:
                logger.error('Unhandled exception: %s' % exc)
                SourceLog.objects.save_status(source=self, status='Error: %s' % exc)                

    class Meta(EmailBaseModel.Meta):
        verbose_name = _(u'IMAP email')
        verbose_name_plural = _(u'IMAP email')


class LocalScanner(InteractiveBaseModel):
    # scanner device string to scanner instance cache dict
    _scanner_cache = {}

    class NoSuchScanner(Exception):
        pass

    is_interactive = True
    source_type = SOURCE_CHOICE_LOCAL_SCANNER
    default_icon = IMAGES

    scanner_device = models.CharField(max_length=255, verbose_name=_(u'scanner device'))
    scanner_description = models.CharField(max_length=255, verbose_name=_(u'scanner description'))

    @classmethod
    def get_scanners(cls):
        iscanner = imagescanner.ImageScanner(remote_search=False)
        scanners = iscanner.list_scanners()
        imagescanner.settings.LOGGING_LEVEL = logging.FATAL
        imagescanner.settings.ENABLE_NET_BACKEND = False
        imagescanner.settings.ENABLE_TEST_BACKEND = False
        
        for scanner in scanners:
            LocalScanner._scanner_cache[unicode(scanner._device)] = {
                'scanner': scanner,
                'description': u'%s: %s - %s - %s <%s>' % (scanner.id, scanner.manufacturer, scanner.name, scanner.description, scanner._device)
            }
        
        return scanners
        
    @classmethod
    def get_scanner(cls, device):
        try:
            return cls._scanner_cache[device]
        except KeyError:
            raise cls.NoSuchScanner

    @classmethod
    def get_scanner_choices(cls, description_only=False):
        if description_only:
            template_func = lambda scanner: (scanner['description'])
        else:
            template_func = lambda scanner: (scanner['scanner']._device, scanner['description'])

        return [template_func(scanner) for scanner in LocalScanner._scanner_cache.values()]

    def scanner(self, _fail=False):
        try:
            return LocalScanner._scanner_cache[self.scanner_device]['scanner']
        except KeyError:
            if _fail == False:
                # Refresh the cache before trying one last time
                LocalScanner.get_scanners()
                return self.scanner(_fail=True)
            else:
                raise self.__class__.NoSuchScanner
                
    def scan(self, as_image=False):
        image = self.scanner().scan()
        if as_image:
            return image
        else:
            buf = StringIO()
            image.save(buf, DEFAULT_LOCAL_SCANNER_FILE_FORMAT)
            return PseudoFile(buf, name=unicode(datetime.datetime.now()).replace(u'.', u'_').replace(u' ', u'_'))

            # This code make new_version upload fail, use it for debugging
            #buf = StringIO()
            #buf.write(image.tostring())
            #buf.seek(0)
            #return buf

    class Meta(InteractiveBaseModel.Meta):
        verbose_name = _(u'local scanner')
        verbose_name_plural = _(u'local scanners')


class StagingFolder(InteractiveBaseModel):
    is_interactive = True
    source_type = SOURCE_CHOICE_STAGING
    default_icon = DRIVE

    folder_path = models.CharField(max_length=255, verbose_name=_(u'folder path'), help_text=_(u'Server side filesystem path.'))
    preview_width = models.IntegerField(verbose_name=_(u'preview width'), help_text=_(u'Width value to be passed to the converter backend.'))
    preview_height = models.IntegerField(blank=True, null=True, verbose_name=_(u'preview height'), help_text=_(u'Height value to be passed to the converter backend.'))
    uncompress = models.CharField(max_length=1, choices=SOURCE_INTERACTIVE_UNCOMPRESS_CHOICES, verbose_name=_(u'uncompress'), help_text=_(u'Whether to expand or not compressed archives.'))
    delete_after_upload = models.BooleanField(default=True, verbose_name=_(u'delete after upload'), help_text=_(u'Delete the file after is has been successfully uploaded.'))

    def get_preview_size(self):
        dimensions = []
        dimensions.append(unicode(self.preview_width))
        if self.preview_height:
            dimensions.append(unicode(self.preview_height))

        return DIMENSION_SEPARATOR.join(dimensions)

    class Meta(InteractiveBaseModel.Meta):
        verbose_name = _(u'staging folder')
        verbose_name_plural = _(u'staging folders')

"""
class SourceMetadata(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    metadata_type = models.ForeignKey(MetadataType, verbose_name=_(u'metadata type'))
    value = models.CharField(max_length=256, blank=True, verbose_name=_(u'value'))

    def __unicode__(self):
        return self.source

    class Meta:
        verbose_name = _(u'source metadata')
        verbose_name_plural = _(u'sources metadata')
"""


class WebForm(InteractiveBaseModel):
    is_interactive = True
    source_type = SOURCE_CHOICE_WEB_FORM
    default_icon = DISK

    uncompress = models.CharField(max_length=1, choices=SOURCE_INTERACTIVE_UNCOMPRESS_CHOICES, verbose_name=_(u'uncompress'), help_text=_(u'Whether to expand or not compressed archives.'))
    #Default path

    class Meta(InteractiveBaseModel.Meta):
        verbose_name = _(u'web form')
        verbose_name_plural = _(u'web forms')


class WatchFolder(BaseModel):
    is_interactive = False
    source_type = SOURCE_CHOICE_WATCH

    folder_path = models.CharField(max_length=255, verbose_name=_(u'folder path'), help_text=_(u'Server side filesystem path.'))
    uncompress = models.CharField(max_length=1, choices=SOURCE_UNCOMPRESS_CHOICES, verbose_name=_(u'uncompress'), help_text=_(u'Whether to expand or not compressed archives.'))
    delete_after_upload = models.BooleanField(default=True, verbose_name=_(u'delete after upload'), help_text=_(u'Delete the file after is has been successfully uploaded.'))
    interval = models.PositiveIntegerField(verbose_name=_(u'interval'), help_text=_(u'Inverval in seconds where the watch folder path is checked for new documents.'))

    def save(self, *args, **kwargs):
        #if self.pk:
        #    remove_job(self.internal_name())
        super(WatchFolder, self).save(*args, **kwargs)
        self.schedule()

    def schedule(self):
        pass
        #if self.enabled:
        #    sources_scheduler.add_interval_job(self.internal_name(),
        #        title=self.fullname(), function=self.execute,
        #        seconds=self.interval, kwargs={'source_id': self.pk}
        #    )

    def execute(self, source_id):
        source = WatchFolder.objects.get(pk=source_id)
        if source.uncompress == SOURCE_UNCOMPRESS_CHOICE_Y:
            expand = True
        else:
            expand = False
        print 'execute: %s' % self.internal_name()

    class Meta(BaseModel.Meta):
        verbose_name = _(u'watch folder')
        verbose_name_plural = _(u'watch folders')


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
    order = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name=_(u'order'), db_index=True)
    #transformation = models.CharField(choices=get_available_transformations_choices(), max_length=128, verbose_name=_(u'transformation'))
    transformation = models.CharField(max_length=128, verbose_name=_(u'transformation'))
    arguments = models.TextField(blank=True, null=True, verbose_name=_(u'arguments'), help_text=_(u'Use dictionaries to indentify arguments, example: %s') % u'{\'degrees\':90}', validators=[ArgumentsValidator()])

    objects = models.Manager()
    transformations = SourceTransformationManager()

    def __unicode__(self):
        #return u'"%s" for %s' % (self.get_transformation_display(), unicode(self.content_object))
        return self.get_transformation_display()

    class Meta:
        ordering = ('order',)
        verbose_name = _(u'document source transformation')
        verbose_name_plural = _(u'document source transformations')


class OutOfProcess(BaseModel):
    is_interactive = False

    class Meta(BaseModel.Meta):
        verbose_name = _(u'out of process')
        verbose_name_plural = _(u'out of process')
