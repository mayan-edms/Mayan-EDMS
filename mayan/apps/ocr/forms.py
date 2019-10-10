from __future__ import unicode_literals

from django import forms
from django.utils.encoding import force_text
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _, ugettext

from mayan.apps.common.widgets import TextAreaDiv

from .models import DocumentVersionPageOCRContent


class DocumentPageOCRContentForm(forms.Form):
    contents = forms.CharField(
        label=_('Contents'),
        widget=TextAreaDiv(
            attrs={
                'class': 'text_area_div full-height',
                'data-height-difference': 360
            }
        )
    )

    def __init__(self, *args, **kwargs):
        page = kwargs.pop('instance', None)
        super(DocumentPageOCRContentForm, self).__init__(*args, **kwargs)
        content = ''
        self.fields['contents'].initial = ''

        content = conditional_escape(
            force_text(self.get_instance_ocr_content(instance=page))
        )

        self.fields['contents'].initial = mark_safe(content)

    def get_instance_ocr_content(self, instance):
        try:
            return instance.content_object.ocr_content.content
        except DocumentVersionPageOCRContent.DoesNotExist:
            return ''


class DocumentVersionPageOCRContentForm(DocumentPageOCRContentForm):
    def get_instance_ocr_content(self, instance):
        try:
            return instance.ocr_content.content
        except (AttributeError, DocumentVersionPageOCRContent.DoesNotExist):
            return ''


class DocumentOCRContentForm(forms.Form):
    """
    Form that concatenates all of a document pages' text content into a
    single textarea widget
    """
    contents = forms.CharField(
        label=_('Contents'),
        widget=TextAreaDiv(
            attrs={
                'class': 'text_area_div full-height',
                'data-height-difference': 360
            }
        )
    )

    def __init__(self, *args, **kwargs):
        document = kwargs.pop('instance', None)
        super(DocumentOCRContentForm, self).__init__(*args, **kwargs)
        content = []
        self.fields['contents'].initial = ''

        for document_page in document.pages.all():
            try:
                page_content = document_page.content_object.ocr_content.content
            except (AttributeError, DocumentVersionPageOCRContent.DoesNotExist):
                pass
            else:
                content.append(conditional_escape(force_text(page_content)))
                content.append(
                    '\n\n\n<hr/><div class="document-page-content-divider">- %s -</div><hr/>\n\n\n' % (
                        ugettext(
                            'Page %(page_number)d'
                        ) % {'page_number': document_page.page_number}
                    )
                )

        self.fields['contents'].initial = mark_safe(''.join(content))
