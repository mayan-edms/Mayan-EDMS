from django import forms

from .widgets import (
    DocumentFilePagesCarouselWidget, DocumentFilePageImageWidget,
    DocumentVersionPagesCarouselWidget, DocumentVersionPageImageWidget,
    ThumbnailFormWidget
)


class DocumentField(forms.fields.Field):
    widget = DocumentVersionPagesCarouselWidget


class DocumentFileField(forms.fields.Field):
    widget = DocumentFilePagesCarouselWidget


class DocumentFilePageField(forms.fields.Field):
    widget = DocumentFilePageImageWidget


class DocumentVersionField(forms.fields.Field):
    widget = DocumentVersionPagesCarouselWidget


class DocumentVersionPageField(forms.fields.Field):
    widget = DocumentVersionPageImageWidget


class ThumbnailFormField(forms.fields.Field):
    widget = ThumbnailFormWidget
