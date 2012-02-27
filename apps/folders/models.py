from datetime import datetime

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from documents.models import Document


class Folder(models.Model):
    title = models.CharField(max_length=128, verbose_name=_(u'title'), db_index=True)
    user = models.ForeignKey(User, verbose_name=_(u'user'))
    datetime_created = models.DateTimeField(verbose_name=_(u'datetime created'))

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            self.datetime_created = datetime.now()
        super(Folder, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('folder_view', [self.pk])

    @property
    def documents(self):
        return Document.objects.filter(folderdocument__folder=self)

    def remove_document(self, document):
        folder_document = self.folderdocument_set.get(document=document)
        folder_document.delete()

    def add_document(self, document):
        folder_document, created = FolderDocument.objects.get_or_create(folder=self, document=document)
        return created

    class Meta:
        unique_together = ('title', 'user')
        ordering = ('title',)
        verbose_name = _(u'folder')
        verbose_name_plural = _(u'folders')


class FolderDocument(models.Model):
    folder = models.ForeignKey(Folder, verbose_name=_('folder'))
    document = models.ForeignKey(Document, verbose_name=_('document'))

    def __unicode__(self):
        return unicode(self.document)

    class Meta:
        verbose_name = _(u'folder document')
        verbose_name_plural = _(u'folders documents')
