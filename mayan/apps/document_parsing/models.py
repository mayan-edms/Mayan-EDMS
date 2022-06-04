from django.db import models
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.models.document_file_page_models import DocumentFilePage
from mayan.apps.documents.models.document_type_models import DocumentType

from .managers import DocumentFilePageContentManager, DocumentTypeSettingsManager


class DocumentFilePageContent(models.Model):
    """
    This model store's the parsed content of a document page.
    """
    document_file_page = models.OneToOneField(
        on_delete=models.CASCADE, related_name='content', to=DocumentFilePage,
        verbose_name=_('Document file page')
    )
    content = models.TextField(
        blank=True, help_text=_(
            'The actual text content as extracted by the document '
            'parsing backend.'
        ), verbose_name=_('Content')
    )

    objects = DocumentFilePageContentManager()

    class Meta:
        verbose_name = _('Document file page content')
        verbose_name_plural = _('Document file page contents')

    def __str__(self):
        return force_text(s=self.document_file_page)


class DocumentTypeSettings(models.Model):
    """
    This model stores the parsing settings for a document type.
    """
    document_type = models.OneToOneField(
        on_delete=models.CASCADE, related_name='parsing_settings',
        to=DocumentType, unique=True, verbose_name=_('Document type')
    )
    auto_parsing = models.BooleanField(
        default=True, verbose_name=_(
            'Automatically queue newly created documents for parsing.'
        )
    )

    objects = DocumentTypeSettingsManager()

    def natural_key(self):
        return self.document_type.natural_key()
    natural_key.dependencies = ['documents.DocumentType']

    class Meta:
        verbose_name = _('Document type settings')
        verbose_name_plural = _('Document types settings')
