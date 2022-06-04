import logging

from django import forms
from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.converter.layers import layer_decorations
from mayan.apps.converter.transformations import (
    BaseTransformation, ImagePasteCoordinatesPercentTransformationMixin
)

logger = logging.getLogger(name=__name__)


class SignatureCapturePasteTransformation(
    ImagePasteCoordinatesPercentTransformationMixin, BaseTransformation
):
    label = _('Paste a signature capture (percent coordinates)')
    name = 'paste_signature_capture_percent'

    @staticmethod
    def get_document(page_object):
        try:
            return page_object.document_file.document
        except AttributeError:
            return page_object.document_version.document

    @classmethod
    def get_arguments(cls):
        arguments = super().get_arguments() + ('internal_name',)
        return arguments

    @classmethod
    def get_form_class(cls):
        SuperForm = super().get_form_class()

        class Form(SuperForm):
            internal_name = forms.ChoiceField(
                help_text=_('Signature capture internal name'),
                label=_('Internal name'),
                required=True
            )

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                def get_choices():
                    try:
                        page_object = self.view.external_object
                    except AttributeError:
                        page_object = self.view.object.object_layer.content_object

                    document = SignatureCapturePasteTransformation.get_document(
                        page_object=page_object
                    )
                    queryset = apps.get_model(
                        app_label='signature_captures',
                        model_name='SignatureCapture'
                    ).valid.filter(document=document)

                    for instance in queryset.all():
                        yield (instance.internal_name, instance)

                self.fields['internal_name'].choices = get_choices()

        return Form

    def get_model_instance(self):
        SignatureCapture = apps.get_model(
            app_label='signature_captures', model_name='SignatureCapture'
        )

        document = SignatureCapturePasteTransformation.get_document(
            page_object=self.object_layer.content_object
        )

        try:
            kwargs = {
                'document': document, 'internal_name': self.internal_name
            }
            instance = SignatureCapture.objects.get(**kwargs)
        except SignatureCapture.DoesNotExist:
            logger.error('Signature capture with not found.; %s', kwargs)
            raise
        else:
            return instance


BaseTransformation.register(
    layer=layer_decorations, transformation=SignatureCapturePasteTransformation
)
