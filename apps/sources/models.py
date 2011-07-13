from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from documents.models import DocumentType
from documents.conf.settings import AVAILABLE_TRANSFORMATIONS
from documents.managers import RecentDocumentManager
from metadata.models import MetadataType

from sources.managers import SourceTransformationManager

available_transformations = ([(name, data['label']) for name, data in AVAILABLE_TRANSFORMATIONS.items()])

SOURCE_UNCOMPRESS_CHOICE_Y = 'y'
SOURCE_UNCOMPRESS_CHOICE_N = 'n'
SOURCE_UNCOMPRESS_CHOICE_ASK = 'a'

SOURCE_UNCOMPRESS_CHOICES = (
    (SOURCE_UNCOMPRESS_CHOICE_Y, _(u'Always')),
    (SOURCE_UNCOMPRESS_CHOICE_N, _(u'Never')),
)

SOURCE_INTERACTIVE_UNCOMPRESS_CHOICES = (
    (SOURCE_UNCOMPRESS_CHOICE_Y, _(u'Always')),
    (SOURCE_UNCOMPRESS_CHOICE_N, _(u'Never')),
    (SOURCE_UNCOMPRESS_CHOICE_ASK, _(u'Ask user'))
)

SOURCE_ICON_DISK = 'disk'
SOURCE_ICON_DATABASE = 'database'
SOURCE_ICON_DRIVE = 'drive'
SOURCE_ICON_DRIVE_NETWORK = 'drive_network'
SOURCE_ICON_DRIVE_USER = 'drive_user'
SOURCE_ICON_EMAIL = 'email'
SOURCE_ICON_FOLDER = 'folder'
SOURCE_ICON_WORLD = 'world'
SOURCE_ICON_PRINTER = 'printer'
SOURCE_ICON_PRINTER_EMPTY = 'printer_empty'

SOURCE_ICON_CHOICES = (
    (SOURCE_ICON_DISK, _(u'Disk')),
    (SOURCE_ICON_DATABASE, _(u'Database')),
    (SOURCE_ICON_DRIVE, _(u'Drive')),
    (SOURCE_ICON_DRIVE_NETWORK, _(u'Network drive')),
    (SOURCE_ICON_DRIVE_USER, _(u'User drive')),
    (SOURCE_ICON_EMAIL, _(u'Envelope')),
    (SOURCE_ICON_FOLDER, _(u'Folder')),
    (SOURCE_ICON_WORLD, _(u'World')),
    (SOURCE_ICON_PRINTER, _(u'Printer')),
    (SOURCE_ICON_PRINTER_EMPTY, _(u'Empty printer')),
)

SOURCE_CHOICE_WEB_FORM = 'webform'
SOURCE_CHOICE_STAGING = 'staging'

SOURCE_CHOICES = (
    (SOURCE_CHOICE_WEB_FORM, _(u'web form')),
    (SOURCE_CHOICE_STAGING, _(u'server staging folder')),
)

SOURCE_CHOICES_PLURAL = (
    (SOURCE_CHOICE_WEB_FORM, _(u'web forms')),
    (SOURCE_CHOICE_STAGING, _(u'server staging folders')),
)


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

        return u'x'.join(dimensions)

    class Meta(InteractiveBaseModel.Meta):
        verbose_name = _(u'staging folder')
        verbose_name_plural = _(u'staging folder')

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


class SourceTransformation(models.Model):
    """
    Model that stores the transformation and transformation arguments
    for a given document source
    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    order = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name=_(u'order'), db_index=True)
    transformation = models.CharField(choices=available_transformations, max_length=128, verbose_name=_(u'transformation'))
    arguments = models.TextField(blank=True, null=True, verbose_name=_(u'arguments'), help_text=_(u'Use dictionaries to indentify arguments, example: {\'degrees\':90}'))

    objects = SourceTransformationManager()

    def __unicode__(self):
        #return u'"%s" for %s' % (self.get_transformation_display(), unicode(self.content_object))
        return self.get_transformation_display()

    class Meta:
        ordering = ('order',)
        verbose_name = _(u'document source transformation')
        verbose_name_plural = _(u'document source transformations')
