import shlex

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.template import Context, Template
from django.urls import reverse
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.module_loading import import_string
from django.utils.six import PY2
from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.models import Document, DocumentType

from .classes import MetadataLookup
from .events import (
    event_document_metadata_added, event_document_metadata_edited,
    event_document_metadata_removed, event_metadata_type_created,
    event_metadata_type_edited, event_metadata_type_relationship
)
from .managers import DocumentTypeMetadataTypeManager, MetadataTypeManager
from .settings import setting_available_parsers, setting_available_validators


def validation_choices():
    return zip(
        setting_available_validators.value,
        setting_available_validators.value
    )


def parser_choices():
    return zip(
        setting_available_parsers.value,
        setting_available_parsers.value
    )


@python_2_unicode_compatible
class MetadataType(models.Model):
    """
    Model to store a type of metadata. Metadata are user defined properties
    that can be assigned a value for each document. Metadata types need
    to be assigned to a document type before they can be used.
    """
    name = models.CharField(
        max_length=48,
        help_text=_(
            'Name used by other apps to reference this metadata type. '
            'Do not use python reserved words, or spaces.'
        ),
        unique=True, verbose_name=_('Name')
    )
    label = models.CharField(
        help_text=_('Short description of this metadata type.'),
        max_length=48, verbose_name=_('Label')
    )
    default = models.CharField(
        blank=True, max_length=128, null=True,
        help_text=_(
            'Enter a template to render. '
            'Use Django\'s default templating language '
            '(https://docs.djangoproject.com/en/1.11/ref/templates/builtins/)'
        ),
        verbose_name=_('Default')
    )
    lookup = models.TextField(
        blank=True, null=True,
        help_text=_(
            'Enter a template to render. '
            'Must result in a comma delimited string. '
            'Use Django\'s default templating language '
            '(https://docs.djangoproject.com/en/1.11/ref/templates/builtins/).'
        ),
        verbose_name=_('Lookup')
    )
    validation = models.CharField(
        blank=True, choices=validation_choices(),
        help_text=_(
            'The validator will reject data entry if the value entered does '
            'not conform to the expected format.'
        ), max_length=64, verbose_name=_('Validator')
    )
    parser = models.CharField(
        blank=True, choices=parser_choices(), help_text=_(
            'The parser will reformat the value entered to conform to the '
            'expected format.'
        ), max_length=64, verbose_name=_('Parser')
    )

    objects = MetadataTypeManager()

    class Meta:
        ordering = ('label',)
        verbose_name = _('Metadata type')
        verbose_name_plural = _('Metadata types')

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return reverse(
            viewname='metadata:setup_metadata_type_edit', kwargs={
                'metadata_type_id': self.pk
            }
        )

    if PY2:
        # Python 2 non unicode version
        @staticmethod
        def comma_splitter(string):
            splitter = shlex.shlex(string.encode('utf-8'), posix=True)
            splitter.whitespace = ','.encode('utf-8')
            splitter.whitespace_split = True
            splitter.commenters = ''.encode('utf-8')
            return [force_text(e) for e in splitter]
    else:
        # Python 3 unicode version
        @staticmethod
        def comma_splitter(string):
            splitter = shlex.shlex(string, posix=True)
            splitter.whitespace = ','
            splitter.whitespace_split = True
            splitter.commenters = ''
            return [force_text(e) for e in splitter]

    def get_default_value(self):
        template = Template(self.default)
        context = Context()
        return template.render(context=context)

    def get_lookup_values(self):
        template = Template(self.lookup)
        context = Context(MetadataLookup.get_as_context())
        return MetadataType.comma_splitter(template.render(context=context))

    def get_required_for(self, document_type):
        """
        Return a queryset of metadata types that are required for the
        specified document type.
        """
        return document_type.metadata.filter(
            required=True, metadata_type=self
        ).exists()

    def natural_key(self):
        return (self.name,)

    def save(self, *args, **kwargs):
        _user = kwargs.pop('_user', None)
        created = not self.pk

        with transaction.atomic():
            result = super(MetadataType, self).save(*args, **kwargs)

            if created:
                event_metadata_type_created.commit(
                    actor=_user, target=self
                )
            else:
                event_metadata_type_edited.commit(
                    actor=_user, target=self
                )

            return result

    def validate_value(self, document_type, value):
        # Check default
        if not value and self.default:
            value = self.get_default_value()

        if not value and self.get_required_for(document_type=document_type):
            raise ValidationError(
                _('"%s" is required for this document type.') % self.label
            )

        if self.lookup:
            lookup_options = self.get_lookup_values()

            if value and value not in lookup_options:
                raise ValidationError(
                    _('Value is not one of the provided options.')
                )

        if self.validation:
            validator = import_string(dotted_path=self.validation)()
            validator.validate(value)

        if self.parser:
            parser = import_string(dotted_path=self.parser)()
            value = parser.parse(value)

        return value


@python_2_unicode_compatible
class DocumentMetadata(models.Model):
    """
    Model used to link an instance of a metadata type with a value to a
    document.
    """
    document = models.ForeignKey(
        on_delete=models.CASCADE, related_name='metadata', to=Document,
        verbose_name=_('Document')
    )
    metadata_type = models.ForeignKey(
        on_delete=models.CASCADE, to=MetadataType, verbose_name=_('Type')
    )
    value = models.CharField(
        blank=True, db_index=True, help_text=_(
            'The actual value stored in the metadata type field for '
            'the document.'
        ), max_length=255, null=True, verbose_name=_('Value')
    )

    class Meta:
        ordering = ('metadata_type',)
        unique_together = ('document', 'metadata_type')
        verbose_name = _('Document metadata')
        verbose_name_plural = _('Document metadata')

    def __str__(self):
        return force_text(self.metadata_type)

    def clean_fields(self, *args, **kwargs):
        super(DocumentMetadata, self).clean_fields(*args, **kwargs)

        self.value = self.metadata_type.validate_value(
            document_type=self.document.document_type, value=self.value
        )

    def delete(self, enforce_required=True, *args, **kwargs):
        """
        Delete a metadata from a document. enforce_required which defaults
        to True, prevents deletion of required metadata at the model level.
        It used set to False when deleting document metadata on document
        type change.
        """
        if enforce_required and self.document.document_type.metadata.filter(required=True).filter(metadata_type=self.metadata_type).exists():
            raise ValidationError(
                _('Metadata type is required for this document type.')
            )

        _user = kwargs.pop('_user', None)
        with transaction.atomic():
            result = super(DocumentMetadata, self).delete(*args, **kwargs)

            event_document_metadata_removed.commit(
                action_object=self.metadata_type, actor=_user,
                target=self.document,
            )
            return result

    def natural_key(self):
        return self.document.natural_key() + self.metadata_type.natural_key()
    natural_key.dependencies = ['documents.Document', 'metadata.MetadataType']

    @property
    def is_required(self):
        """
        Return a boolean value of True of this metadata instance's parent type
        is required for the stored document type.
        """
        return self.metadata_type.get_required_for(
            document_type=self.document.document_type
        )

    def save(self, *args, **kwargs):
        if self.metadata_type.pk not in self.document.document_type.metadata.values_list('metadata_type', flat=True):
            raise ValidationError(
                _('Metadata type is not valid for this document type.')
            )

        _user = kwargs.pop('_user', None)
        created = not self.pk

        with transaction.atomic():
            result = super(DocumentMetadata, self).save(*args, **kwargs)

            if created:
                event_document_metadata_added.commit(
                    action_object=self.metadata_type, actor=_user,
                    target=self.document,
                )
            else:
                event_document_metadata_edited.commit(
                    action_object=self.metadata_type, actor=_user,
                    target=self.document,
                )

            return result


@python_2_unicode_compatible
class DocumentTypeMetadataType(models.Model):
    """
    Model used to store the relationship between a metadata type and a
    document type.
    """
    document_type = models.ForeignKey(
        on_delete=models.CASCADE, related_name='metadata', to=DocumentType,
        verbose_name=_('Document type')
    )
    metadata_type = models.ForeignKey(
        on_delete=models.CASCADE, to=MetadataType,
        verbose_name=_('Metadata type')
    )
    required = models.BooleanField(default=False, verbose_name=_('Required'))

    objects = DocumentTypeMetadataTypeManager()

    class Meta:
        ordering = ('metadata_type',)
        unique_together = ('document_type', 'metadata_type')
        verbose_name = _('Document type metadata type options')
        verbose_name_plural = _('Document type metadata types options')

    def __str__(self):
        return force_text(self.metadata_type)

    def delete(self, *args, **kwargs):
        _user = kwargs.pop('_user', None)

        with transaction.atomic():
            result = super(DocumentTypeMetadataType, self).delete(*args, **kwargs)

            event_metadata_type_relationship.commit(
                action_object=self.document_type, actor=_user,
                target=self.metadata_type,
            )

            return result

    def save(self, *args, **kwargs):
        _user = kwargs.pop('_user', None)

        with transaction.atomic():
            result = super(DocumentTypeMetadataType, self).save(*args, **kwargs)

            event_metadata_type_relationship.commit(
                action_object=self.document_type, actor=_user,
                target=self.metadata_type,
            )

            return result
