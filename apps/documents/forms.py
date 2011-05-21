from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.conf import settings

from common.wizard import BoundFormWizard
from common.forms import DetailForm
from common.literals import PAGE_SIZE_CHOICES, PAGE_ORIENTATION_CHOICES
from common.conf.settings import DEFAULT_PAPER_SIZE
from common.conf.settings import DEFAULT_PAGE_ORIENTATION
from common.utils import urlquote
from metadata.models import MetadataSet, MetadataType
from metadata.forms import MetadataFormSet

from documents.models import Document, DocumentType, \
    DocumentPage, DocumentPageTransformation


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


class ImageWidget(forms.widgets.Widget):
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


#TODO: Turn this into a base form and let others inherit
class DocumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            document_type = kwargs['initial'].get('document_type', None)
            if document_type:
                if 'document_type' in self.fields:
                    #To allow merging with DocumentForm_edit
                    self.fields['document_type'].widget = forms.HiddenInput()
                filenames_qs = kwargs['initial']['document_type'].documenttypefilename_set.filter(enabled=True)
                if filenames_qs.count() > 0:
                    self.fields['document_type_available_filenames'] = forms.ModelChoiceField(
                        queryset=filenames_qs,
                        required=False,
                        label=_(u'Quick document rename'))

    class Meta:
        model = Document
        exclude = ('description', 'tags', 'document_type')

    new_filename = forms.CharField(
        label=_('New document filename'), required=False
    )


class DocumentPreviewForm(forms.Form):
    def __init__(self, *args, **kwargs):
        document = kwargs.pop('document', None)
        super(DocumentPreviewForm, self).__init__(*args, **kwargs)
        self.fields['preview'].initial = document
        self.fields['preview'].label = _(u'Document pages (%s)') % document.documentpage_set.count()

    preview = forms.CharField(widget=ImageWidget())


class DocumentContentForm(forms.Form):
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


class DocumentForm_view(DetailForm):
    class Meta:
        model = Document
        exclude = ('file', 'tags')


class DocumentForm_edit(DocumentForm):
    class Meta:
        model = Document
        exclude = ('file', 'document_type', 'tags')


class StagingDocumentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        cls = kwargs.pop('cls')
        super(StagingDocumentForm, self).__init__(*args, **kwargs)
        try:
            self.fields['staging_file_id'].choices = [
                (staging_file.id, staging_file) for staging_file in cls.get_all()
            ]
        except:
            pass

        if 'initial' in kwargs:
            document_type = kwargs['initial'].get('document_type', None)
            if document_type:
                filenames_qs = kwargs['initial']['document_type'].documenttypefilename_set.filter(enabled=True)
                if filenames_qs.count() > 0:
                    self.fields['document_type_available_filenames'] = forms.ModelChoiceField(
                        queryset=filenames_qs,
                        required=False,
                        label=_(u'Quick document rename'))

    staging_file_id = forms.ChoiceField(label=_(u'Staging file'))
    new_filename = forms.CharField(
        label=_('New document filename'), required=False
    )


class DocumentTypeSelectForm(forms.Form):
    document_type = forms.ModelChoiceField(queryset=DocumentType.objects.all(), label=(u'Document type'), required=False)


class DocumentCreateWizard(BoundFormWizard):
    def generate_metadata_initial_values(self):
        initial = []
        for metadata_type in self.metadata_types:
            initial.append({
                'metadata_type': metadata_type,
            })

        for metadata_set in self.metadata_sets:
            for metadata_set_item in metadata_set.metadatasetitem_set.all():
                data = {
                    'metadata_type': metadata_set_item.metadata_type,
                }
                if data not in initial:
                    initial.append(data)

        return initial

    def __init__(self, *args, **kwargs):
        self.query_dict = {}
        self.multiple = kwargs.pop('multiple', True)
        self.step_titles = kwargs.pop('step_titles', [
            _(u'step 1 of 3: Document type'),
            _(u'step 2 of 3: Metadata selection'),
            _(u'step 3 of 3: Document metadata'),
            ])
        self.document_type = kwargs.pop('document_type', None)

        super(DocumentCreateWizard, self).__init__(*args, **kwargs)

        if self.document_type:
            self.initial = {0: self.generate_metadata_initial_values()}

    def render_template(self, request, form, previous_fields, step, context=None):
        context = {'step_title': self.extra_context['step_titles'][step]}
        return super(DocumentCreateWizard, self).render_template(
            request, form, previous_fields, step, context
        )

    def parse_params(self, request, *args, **kwargs):
        self.extra_context = {'step_titles': self.step_titles}

    def process_step(self, request, form, step):
        if isinstance(form, DocumentTypeSelectForm):
            self.document_type = form.cleaned_data['document_type']

        if isinstance(form, MetadataSelectionForm):
            self.metadata_sets = form.cleaned_data['metadata_sets']
            self.metadata_types = form.cleaned_data['metadata_types']
            initial_data = self.generate_metadata_initial_values()
            self.initial = {2: initial_data}
            if not initial_data:
                # If there is no metadata selected end wizard
                self.form_list = [DocumentTypeSelectForm, MetadataSelectionForm]

        if isinstance(form, MetadataFormSet):
            for identifier, metadata in enumerate(form.cleaned_data):
                self.query_dict['metadata%s_id' % identifier] = metadata['id']
                self.query_dict['metadata%s_value' % identifier] = metadata['value']

    def get_template(self, step):
        return 'generic_wizard.html'

    def done(self, request, form_list):
        if self.multiple:
            view = 'upload_document_multiple'
        else:
            view = 'upload_document'

        if self.document_type:
            self.query_dict['document_type_id'] = self.document_type.pk

        url = urlquote(reverse(view), self.query_dict)
        return HttpResponseRedirect(url)


class PrintForm(forms.Form):
    page_size = forms.ChoiceField(choices=PAGE_SIZE_CHOICES, initial=DEFAULT_PAPER_SIZE, label=_(u'Page size'), required=False)
    custom_page_width = forms.CharField(label=_(u'Custom page width'), required=False)
    custom_page_height = forms.CharField(label=_(u'Custom page height'), required=False)
    page_orientation = forms.ChoiceField(choices=PAGE_ORIENTATION_CHOICES, initial=DEFAULT_PAGE_ORIENTATION, label=_(u'Page orientation'), required=True)
    page_range = forms.CharField(label=_(u'Page range'), required=False)


class MetadataSelectionForm(forms.Form):
    metadata_sets = forms.ModelMultipleChoiceField(
        queryset=MetadataSet.objects.all(),
        label=_(u'Metadata sets'),
        required=False,
        widget=forms.widgets.SelectMultiple(attrs={'size': 10, 'class': 'choice_form'})
    )

    metadata_types = forms.ModelMultipleChoiceField(
        queryset=MetadataType.objects.all(),
        label=_(u'Metadata'),
        required=False,
        widget=forms.widgets.SelectMultiple(attrs={'size': 10, 'class': 'choice_form'})
    )
