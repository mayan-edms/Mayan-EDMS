from django.db import models
from django.utils.translation import ugettext_lazy as _

from documents.models import DocumentType
from metadata.models import MetadataType


SOURCE_UMCOMPRESS_CHOICE_Y = 'y'
SOURCE_UMCOMPRESS_CHOICE_N = 'n'
SOURCE_UMCOMPRESS_CHOICE_ASK = 'a'

SOURCE_UNCOMPRESS_CHOICES = (
    (SOURCE_UMCOMPRESS_CHOICE_Y, _(u'Yes')),
    (SOURCE_UMCOMPRESS_CHOICE_N, _(u'No')),
)

SOURCE_INTERACTIVE_UNCOMPRESS_CHOICES = (
    (SOURCE_UMCOMPRESS_CHOICE_Y, _(u'Yes')),
    (SOURCE_UMCOMPRESS_CHOICE_N, _(u'No')),
    (SOURCE_UMCOMPRESS_CHOICE_ASK, _(u'Ask'))
)

SOURCE_ICON_DISK = 'disk'
SOURCE_ICON_DATABASE = 'database'
SOURCE_ICON_DRIVE = 'drive'
SOURCE_ICON_DRIVE_NETWORK = 'drive_network'
SOURCE_ICON_DRIVE_USER = 'drive_user'
SOURCE_ICON_EMAIL = 'email'
SOURCE_ICON_FOLDER = 'folder'
SOURCE_ICON_WORLD = 'world'

SOURCE_ICON_CHOICES = (
    (SOURCE_ICON_DISK, _(u'disk')),
    (SOURCE_ICON_DATABASE, _(u'database')),
    (SOURCE_ICON_DRIVE, _(u'drive')),
    (SOURCE_ICON_DRIVE_NETWORK, _(u'network drive')),
    (SOURCE_ICON_DRIVE_USER, _(u'user drive')),
    (SOURCE_ICON_EMAIL, _(u'envelope')),
    (SOURCE_ICON_FOLDER, _(u'folder')),
    (SOURCE_ICON_WORLD, _(u'world'))
)

SOURCE_CHOICE_WEB_FORM = 'wform'
SOURCE_CHOICE_STAGING = 'stagn'
    
SOURCE_CHOICES = (
    (SOURCE_CHOICE_WEB_FORM, _(u'Web form')),
    (SOURCE_CHOICE_STAGING, _(u'Server staging folder')),
)


class BaseModel(models.Model):
    title = models.CharField(max_length=64, verbose_name=_(u'title'))
    enabled = models.BooleanField(default=True, verbose_name=_(u'enabled'))
    whitelist = models.TextField(blank=True, verbose_name=_(u'whitelist'))
    blacklist = models.TextField(blank=True, verbose_name=_(u'blacklist'))
    document_type = models.ForeignKey(DocumentType, blank=True, null=True, verbose_name=_(u'document type'))
    
    # M2M
    # Default Metadata sets
    # Default Metadata types & default values

    def __unicode__(self):
        return u'%s (%s)' % (self.title, dict(SOURCE_CHOICES).get(self.source_type))    

    class Meta:
        ordering = ['title']
        abstract = True


#class MetadataValue(models.Model):
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


class InteractiveBaseModel(BaseModel):
    icon = models.CharField(blank=True, null=True, max_length=24, choices=SOURCE_ICON_CHOICES, verbose_name=_(u'icon'))

    def save(self, *args, **kwargs):
        if not self.icon:
            self.icon = self.default_icon
        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True

        
class StagingFolder(InteractiveBaseModel):
    is_interactive = True
    source_type = SOURCE_CHOICE_STAGING
    default_icon = SOURCE_ICON_DRIVE
    
    folder_path = models.CharField(max_length=255, verbose_name=_(u'folder path'))
    preview_width = models.IntegerField(verbose_name=_(u'preview width'))
    preview_height = models.IntegerField(blank=True, null=True, verbose_name=_(u'preview height'))
    uncompress = models.CharField(max_length=1, choices=SOURCE_INTERACTIVE_UNCOMPRESS_CHOICES, verbose_name=_(u'uncompress'))
    delete_after_upload = models.BooleanField(default=True, verbose_name=_(u'delete after upload'))
    
    class Meta:
        verbose_name = _(u'staging folder')
        verbose_name_plural = _(u'staging folder')    
    

class WebForm(InteractiveBaseModel):
    is_interactive = True
    source_type = SOURCE_CHOICE_WEB_FORM
    default_icon = SOURCE_ICON_DISK

    uncompress = models.CharField(max_length=1, choices=SOURCE_INTERACTIVE_UNCOMPRESS_CHOICES, verbose_name=_(u'uncompress'))
    #Default path

    class Meta:
        verbose_name = _(u'web form')
        verbose_name_plural = _(u'web forms')    
