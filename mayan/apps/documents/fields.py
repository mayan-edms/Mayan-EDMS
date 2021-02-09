from django import forms

from .widgets import (
    DocumentFilePagesCarouselWidget, DocumentVersionPagesCarouselWidget,
    PageImageWidget, ThumbnailFormWidget
)


class DocumentFileField(forms.fields.Field):
    widget = DocumentFilePagesCarouselWidget


class DocumentFilePageField(forms.fields.Field):
    widget = PageImageWidget


class DocumentVersionField(forms.fields.Field):
    widget = DocumentVersionPagesCarouselWidget


class DocumentVersionPageField(forms.fields.Field):
    widget = PageImageWidget


class ThumbnailFormField(forms.fields.Field):
    widget = ThumbnailFormWidget
