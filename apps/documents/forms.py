from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.conf import settings

from common.forms import DetailForm
from common.literals import PAGE_SIZE_CHOICES, PAGE_ORIENTATION_CHOICES
from common.conf.settings import DEFAULT_PAPER_SIZE
from common.conf.settings import DEFAULT_PAGE_ORIENTATION

from documents.models import Document, DocumentType, \
    DocumentPage, DocumentPageTransformation, DocumentTypeFilename


# Document page forms
class DocumentPageTransformationForm(forms.ModelForm):
    class Meta:
        model = DocumentPageTransformation

    def __init__(self, *args, **kwargs):
        super(DocumentPageTransformationForm, self).__init__(*args, **kwargs)
        self.fields['document_page'].widget = forms.HiddenInput()


class DocumentPageImageWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)
        zoom = final_attrs.get('zoom', 100)
        rotation = final_attrs.get('rotation', 0)
        if value:
            output = []
            output.append('''
                <div class="full-height scrollable" style="overflow: auto;">
                    <div class="tc">
                        <img class="lazy-load" data-href="%(img)s?page=%(page)d&zoom=%(zoom)d&rotation=%(rotation)d" src="%(media_url)s/images/ajax-loader.gif" alt="%(string)s" />
                        <noscript>
                            <img src="%(img)s?page=%(page)d&zoom=%(zoom)d&rotation=%(rotation)d" alt="%(string)s" />
                        </noscript>
                    </div>
                </div>''' % {
                'img': reverse('document_display', args=[value.document.id]),
                'page': value.page_number,
                'zoom': zoom,
                'rotation': rotation,
                'media_url': settings.MEDIA_URL,
                'string': ugettext(u'page image')
                })
            return mark_safe(u''.join(output))
        else:
            return u''


class DocumentPageForm(DetailForm):
    class Meta:
        model = DocumentPage
        exclude = ('document', 'document_type', 'page_label', 'content')

    def __init__(self, *args, **kwargs):
        zoom = kwargs.pop('zoom', 100)
        rotation = kwargs.pop('rotation', 0)
        super(DocumentPageForm, self).__init__(*args, **kwargs)
        self.fields['page_image'].initial = self.instance
        self.fields['page_image'].widget.attrs.update({
            'zoom': zoom,
            'rotation': rotation
        })

    page_image = forms.CharField(
        label=_(u'Page image'), widget=DocumentPageImageWidget()
    )


class DocumentPageForm_text(DetailForm):
    class Meta:
        model = DocumentPage
        fields = ('page_label', 'content')

    content = forms.CharField(
        label=_(u'Contents'),
        widget=forms.widgets.Textarea(attrs={
            'rows': 18, 'cols': 80, 'readonly': 'readonly'
        }))


class DocumentPageForm_edit(forms.ModelForm):
    class Meta:
        model = DocumentPage
        fields = ('page_label', 'content')

    def __init__(self, *args, **kwargs):
        super(DocumentPageForm_edit, self).__init__(*args, **kwargs)
        self.fields['page_image'].initial = self.instance
        self.fields.keyOrder = [
            'page_image',
            'page_label',
            'content',
        ]
    page_image = forms.CharField(
        required=False, widget=DocumentPageImageWidget()
    )


# Document forms
class DocumentPagesCarouselWidget(forms.widgets.Widget):
    """
    Display many small representations of a document pages
    """
    def render(self, name, value, attrs=None):
        output = []
        output.append(u'<div style="white-space:nowrap; overflow: auto;">')

        for page in value.documentpage_set.all():
            output.append(
                u'''<div style="display: inline-block; margin: 5px 10px 10px 10px;">
                        <div class="tc">%(page_string)s %(page)s</div>
                        <div class="tc" style="border: 1px solid black; margin: 5px 0px 5px 0px;">
                            <a rel="page_gallery" class="fancybox-noscaling" href="%(view_url)s?page=%(page)d">
                                <img class="lazy-load" data-href="%(img)s?page=%(page)d" src="%(media_url)s/images/ajax-loader.gif" alt="%(string)s" />
                                <noscript>
                                    <img src="%(img)s?page=%(page)d" alt="%(string)s" />
                                </noscript>
                            </a>
                        </div>
                        <div class="tc">
                            <a class="fancybox-iframe" href="%(url)s"><span class="famfam active famfam-page_white_go"></span>%(details_string)s</a>
                        </div>
                    </div>''' % {
                    'url': reverse('document_page_view', args=[page.pk]),
                    'img': reverse('document_preview_multipage', args=[value.pk]),
                    'page': page.page_number,
                    'view_url': reverse('document_display', args=[page.document.pk]),
                    'page_string': ugettext(u'Page'),
                    'details_string': ugettext(u'Details'),
                    'media_url': settings.MEDIA_URL,
                    'string': _(u'document page')
                })

        output.append(u'</div>')
        output.append(
            u'<br /><span class="famfam active famfam-magnifier"></span>%s' %
             ugettext(u'Click on the image for full size preview'))

        return mark_safe(u''.join(output))


class DocumentPreviewForm(forms.Form):
    def __init__(self, *args, **kwargs):
        document = kwargs.pop('document', None)
        super(DocumentPreviewForm, self).__init__(*args, **kwargs)
        self.fields['preview'].initial = document
        self.fields['preview'].label = _(u'Document pages (%s)') % document.documentpage_set.count()

    preview = forms.CharField(widget=DocumentPagesCarouselWidget())


class DocumentForm(forms.ModelForm):
    """
    Baseform for document creation, and editing, made generic enough to
    be used by document creation from staging files
    """
    class Meta:
        model = Document
        exclude = ('description', 'tags', 'document_type')

    def __init__(self, *args, **kwargs):
        document_type = kwargs.pop('document_type', None)
        instance = kwargs.pop('instance', None)

        super(DocumentForm, self).__init__(*args, **kwargs)

        if 'document_type' in self.fields:
            # To allow merging with DocumentForm_edit
            self.fields['document_type'].widget = forms.HiddenInput()

        # Instance's document_type overrides the passed document_type
        if instance:
            if hasattr(instance, 'document_type'):
                document_type = instance.document_type
                
        if document_type:
            filenames_qs = document_type.documenttypefilename_set.filter(enabled=True)
            if filenames_qs.count() > 0:
                self.fields['document_type_available_filenames'] = forms.ModelChoiceField(
                    queryset=filenames_qs,
                    required=False,
                    label=_(u'Quick document rename'))
                    
        # Put the expand field last in the field order list
        expand_field_index = self.fields.keyOrder.index('expand')
        expand_field = self.fields.keyOrder.pop(expand_field_index)
        self.fields.keyOrder.append(expand_field)                    

    new_filename = forms.CharField(
        label=_('New document filename'), required=False
    )

    expand = forms.BooleanField(
        label=_(u'Expand compressed files'), required=False, 
        help_text=ugettext(u'Upload a compressed file\'s contained files as individual documents')
    )
    

class DocumentForm_edit(DocumentForm):
    """
    Form sub classes from DocumentForm used only when editing a document
    """
    class Meta:
        model = Document
        exclude = ('file', 'document_type', 'tags', 'expand')

    
    def __init__(self, *args, **kwargs):
        super(DocumentForm_edit, self).__init__(*args, **kwargs)
        self.fields.pop('expand')
        

class DocumentPropertiesForm(DetailForm):
    """
    Detail class form to display a document file based properties
    """
    class Meta:
        model = Document
        exclude = ('file', 'tags')


class DocumentContentForm(forms.Form):
    """
    Form that concatenates all of a document pages' text content into a
    single textarea widget
    """
    def __init__(self, *args, **kwargs):
        self.document = kwargs.pop('document', None)
        super(DocumentContentForm, self).__init__(*args, **kwargs)
        content = []
        self.fields['contents'].initial = u''
        for page in self.document.documentpage_set.all():
            if page.content:
                content.append(page.content)
                content.append(u'\n\n\n - Page %s - \n\n\n' % page.page_number)

        self.fields['contents'].initial = u''.join(content)

    contents = forms.CharField(
        label=_(u'Contents'),
        widget=forms.widgets.Textarea(attrs={
            'rows': 14, 'cols': 80, 'readonly': 'readonly'
        })
    )


class DocumentTypeSelectForm(forms.Form):
    """
    Form to select the document type of a document to be created, used
    as form #1 in the document creation wizard
    """
    document_type = forms.ModelChoiceField(queryset=DocumentType.objects.all(), label=(u'Document type'), required=False)


class PrintForm(forms.Form):
    page_size = forms.ChoiceField(choices=PAGE_SIZE_CHOICES, initial=DEFAULT_PAPER_SIZE, label=_(u'Page size'), required=False)
    custom_page_width = forms.CharField(label=_(u'Custom page width'), required=False)
    custom_page_height = forms.CharField(label=_(u'Custom page height'), required=False)
    page_orientation = forms.ChoiceField(choices=PAGE_ORIENTATION_CHOICES, initial=DEFAULT_PAGE_ORIENTATION, label=_(u'Page orientation'), required=True)
    page_range = forms.CharField(label=_(u'Page range'), required=False)


class StagingDocumentForm(DocumentForm):
    """
    Form that show all the files in the staging folder specified by the
    StagingFile class passed as 'cls' argument
    """
    def __init__(self, *args, **kwargs):
        cls = kwargs.pop('cls')
        super(StagingDocumentForm, self).__init__(*args, **kwargs)
        try:
            self.fields['staging_file_id'].choices = [
                (staging_file.id, staging_file) for staging_file in cls.get_all()
            ]
        except:
            pass

        # Put staging_list field first in the field order list
        staging_list_index = self.fields.keyOrder.index('staging_file_id')
        staging_list = self.fields.keyOrder.pop(staging_list_index)
        self.fields.keyOrder.insert(0, staging_list)

    staging_file_id = forms.ChoiceField(label=_(u'Staging file'))

    class Meta(DocumentForm.Meta):
        exclude = ('description', 'file', 'document_type', 'tags')


class DocumentTypeForm(forms.ModelForm):
    """
    Model class form to create or edit a document type
    """
    class Meta:
        model = DocumentType


class DocumentTypeFilenameForm(forms.ModelForm):
    """
    Model class form to edit a document type filename
    """
    class Meta:
        model = DocumentTypeFilename
        fields = ('filename', 'enabled')


class DocumentTypeFilenameForm_create(forms.ModelForm):
    """
    Model class form to create a new document type filename
    """
    class Meta:
        model = DocumentTypeFilename
        fields = ('filename',)
