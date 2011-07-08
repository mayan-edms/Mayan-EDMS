from django.db import models
from django.utils.translation import ugettext_lazy as _

from documents.models import DocumentType
from metadata.models import MetadataType


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
    (SOURCE_CHOICE_WEB_FORM, _(u'Web form')),
    (SOURCE_CHOICE_STAGING, _(u'Server staging folder')),
)


class BaseModel(models.Model):
    title = models.CharField(max_length=64, verbose_name=_(u'title'))
    enabled = models.BooleanField(default=True, verbose_name=_(u'enabled'))
    whitelist = models.TextField(blank=True, verbose_name=_(u'whitelist'))
    blacklist = models.TextField(blank=True, verbose_name=_(u'blacklist'))
    document_type = models.ForeignKey(DocumentType, blank=True, null=True, verbose_name=_(u'document type'), help_text=(u'Optional document type to be applied to documents uploaded from this source.'))

    def __unicode__(self):
        return u'%s' % self.title
        
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


#class StagingFolderMetadataValue(models.Model):
#    source = models.ForeignKey(BaseModel, verbose_name=_(u'document source'))
#    metadata_type = models.ForeignKey(MetadataType, verbose_name=_(u'metadata type'))
#    value = models.CharField(max_length=256, blank=True, verbose_name=_(u'value'))
#
#    def __unicode__(self):
#        return self.source
#
#    class Meta:
#        verbose_name = _(u'source metadata')
#        verbose_name_plural = _(u'sources metadata')


class WebForm(InteractiveBaseModel):
    is_interactive = True
    source_type = SOURCE_CHOICE_WEB_FORM
    default_icon = SOURCE_ICON_DISK

    uncompress = models.CharField(max_length=1, choices=SOURCE_INTERACTIVE_UNCOMPRESS_CHOICES, verbose_name=_(u'uncompress'), help_text=_(u'Whether to expand or not compressed archives.'))
    #Default path

    class Meta(InteractiveBaseModel.Meta):
        verbose_name = _(u'web form')
        verbose_name_plural = _(u'web forms')
