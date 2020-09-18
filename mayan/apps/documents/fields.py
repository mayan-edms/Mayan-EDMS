from django import forms

from .widgets import (
    DocumentFilePagesCarouselWidget, DocumentFilePageImageWidget
)


class DocumentField(forms.fields.Field):
    widget = DocumentFilePagesCarouselWidget


class DocumentFileField(forms.fields.Field):
    widget = DocumentFilePagesCarouselWidget


class DocumentFilePageField(forms.fields.Field):
    widget = DocumentFilePageImageWidget
