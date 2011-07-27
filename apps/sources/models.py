from ast import literal_eval

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.exceptions import ValidationError

from documents.models import DocumentType
from metadata.models import MetadataType
from converter.api import get_available_transformations_choices
from converter.literals import DIMENSION_SEPARATOR    
from scheduler.api import register_interval_job, remove_job

from sources.managers import SourceTransformationManager
from sources.literals import SOURCE_CHOICES, SOURCE_CHOICES_PLURAL, \
    SOURCE_INTERACTIVE_UNCOMPRESS_CHOICES, SOURCE_CHOICE_WEB_FORM, \
    SOURCE_CHOICE_STAGING, SOURCE_ICON_DISK, SOURCE_ICON_DRIVE, \
    SOURCE_ICON_CHOICES, SOURCE_CHOICE_WATCH, SOURCE_UNCOMPRESS_CHOICES


class BaseModel(models.Model):
    title = models.CharField(max_length=64, verbose_name=_(u'title'))
    enabled = models.BooleanField(default=True, verbose_name=_(u'enabled'))
    whitelist = models.TextField(blank=True, verbose_name=_(u'whitelist'))
    blacklist = models.TextField(blank=True, verbose_name=_(u'blacklist'))
    document_type = models.ForeignKey(DocumentType, blank=True, null=True, verbose_name=_(u'document type'), help_text=(u'Optional document type to be applied to documents uploaded from this source.'))

    def __unicode__(self):
        return u'%s' % self.title
        
    def fullname(self):
        return u' '.join([self.class_fullname(), '"%s"' % self.title])

    @classmethod
    def class_fullname(cls):
        return unicode(dict(SOURCE_CHOICES).get(cls.source_type))

    @classmethod
    def class_fullname_plural(cls):
        return unicode(dict(SOURCE_CHOICES_PLURAL).get(cls.source_type))
        
    class Meta:
        ordering = ('title',)
        abstract = True


class InteractiveBaseModel(BaseModel):
    icon = models.CharField(blank=True, null=True, max_length=24, choices=SOURCE_ICON_CHOICES, verbose_name=_(u'icon'), help_text=_(u'An icon to visually distinguish this source.'))

    def save(self, *args, **kwargs):
        if not self.icon:
            self.icon = self.default_icon
        super(BaseModel, self).save(*args, **kwargs)

    class Meta(BaseModel.Meta):
        abstract = True

        
class StagingFolder(InteractiveBaseModel):
    is_interactive = True
    source_type = SOURCE_CHOICE_STAGING
    default_icon = SOURCE_ICON_DRIVE
    
    folder_path = models.CharField(max_length=255, verbose_name=_(u'folder path'), help_text=_(u'Server side filesystem path.'))
    preview_width = models.IntegerField(blank=True, null=True, verbose_name=_(u'preview width'), help_text=_(u'Width value to be passed to the converter backend.'))
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

'''
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
'''

class WebForm(InteractiveBaseModel):
    is_interactive = True
    source_type = SOURCE_CHOICE_WEB_FORM
    default_icon = SOURCE_ICON_DISK

    uncompress = models.CharField(max_length=1, choices=SOURCE_INTERACTIVE_UNCOMPRESS_CHOICES, verbose_name=_(u'uncompress'), help_text=_(u'Whether to expand or not compressed archives.'))
    #Default path

    class Meta(InteractiveBaseModel.Meta):
        verbose_name = _(u'web form')
        verbose_name_plural = _(u'web forms')

def test():
    print 'WatchFolder'
    
class WatchFolder(BaseModel):
    is_interactive = False
    source_type = SOURCE_CHOICE_WATCH
    
    folder_path = models.CharField(max_length=255, verbose_name=_(u'folder path'), help_text=_(u'Server side filesystem path.'))
    uncompress = models.CharField(max_length=1, choices=SOURCE_UNCOMPRESS_CHOICES, verbose_name=_(u'uncompress'), help_text=_(u'Whether to expand or not compressed archives.'))
    delete_after_upload = models.BooleanField(default=True, verbose_name=_(u'delete after upload'), help_text=_(u'Delete the file after is has been successfully uploaded.'))
    interval = models.PositiveIntegerField(verbose_name=_(u'interval'), help_text=_(u'Inverval in seconds where the watch folder path is checked for new documents.'))
    
    def save(self, *args, **kwargs):
        if self.pk:
            remove_job('watch_folder_%d' % self.pk)
        super(WatchFolder, self).save(*args, **kwargs)
        if self.enabled:
            register_interval_job('watch_folder_%d' % self.pk, self.fullname(), test, seconds=self.interval)

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
    transformation = models.CharField(choices=get_available_transformations_choices(), max_length=128, verbose_name=_(u'transformation'))
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
