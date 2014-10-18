from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext as _

from documents.models import Document
# TODO: Simplify this model by adding a M2M field called documents


class Folder(models.Model):
    title = models.CharField(max_length=128, verbose_name=_(u'Title'), db_index=True)
    user = models.ForeignKey(User, verbose_name=_(u'User'))
    datetime_created = models.DateTimeField(verbose_name=_(u'Datetime created'))

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            self.datetime_created = now()
        super(Folder, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('folders:folder_view', [self.pk])

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
        verbose_name = _(u'Folder')
        verbose_name_plural = _(u'Folders')


class FolderDocument(models.Model):
    folder = models.ForeignKey(Folder, verbose_name=_('Folder'))
    document = models.ForeignKey(Document, verbose_name=_('Document'))

    def __unicode__(self):
        return unicode(self.document)

    class Meta:
        verbose_name = _(u'Folder document')
        verbose_name_plural = _(u'Folders documents')
