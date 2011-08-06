from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.template.defaultfilters import capfirst
from django.conf import settings

from tags.widgets import get_tags_inline_widget


class DocumentGroupImageWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        output = []
        if value['links']:
            output.append(u'<div class="group navform wat-cf">')
            for link in value['links']:
                output.append(u'''
                    <button class="button" type="submit" name="action" value="%(action)s">
                        <span class="famfam active famfam-%(famfam)s"></span>%(text)s
                    </button>
                ''' % {
                    'famfam': link.get('famfam', u'link'),
                    'text': capfirst(link['text']),
                    'action': reverse('document_group_view', args=[value['current_document'].pk, value['group'].pk])
                })
            output.append(u'</div>')

        output.append(u'<div style="white-space:nowrap; overflow: auto;">')
        for document in value['group_data']:
            tags_template = get_tags_inline_widget(document)

            output.append(
                u'''<div style="display: inline-block; margin: 0px 10px 10px 10px; %(current)s">
                        <div class="tc">%(document_name)s</div>
                        <div class="tc">%(page_string)s: %(document_pages)d</div>
                        %(tags_template)s
                        <div class="tc">
                            <a rel="group_%(group_id)d_documents_gallery" class="fancybox-noscaling" href="%(view_url)s">
                                <img class="lazy-load" style="border: 1px solid black; margin: 10px;" src="%(static_url)s/images/ajax-loader.gif" data-href="%(img)s" alt="%(string)s" />
                                <noscript>
                                    <img style="border: 1px solid black; margin: 10px;" src="%(img)s" alt="%(string)s" />
                                </noscript>
                            </a>
                        </div>
                        <div class="tc">
                            <a href="%(url)s"><span class="famfam active famfam-page_go"></span>%(details_string)s</a>
                        </div>
                    </div>''' % {
                    'url': reverse('document_view_simple', args=[document.pk]),
                    'img': reverse('document_preview_multipage', args=[document.pk]),
                    'current': u'border: 5px solid black; padding: 3px;' if value['current_document'] == document else u'',
                    'view_url': reverse('document_display', args=[document.pk]),
                    'document_pages': document.documentpage_set.count(),
                    'page_string': ugettext(u'Pages'),
                    'details_string': ugettext(u'Select'),
                    'group_id': value['group'].pk,
                    'document_name': document,
                    'static_url': settings.STATIC_URL,
                    'tags_template': tags_template if tags_template else u'',
                    'string': _(u'group document'),
                })
        output.append(u'</div>')
        output.append(
            u'<br /><span class="famfam active famfam-magnifier"></span>%s' %
             ugettext(u'Click on the image for full size view of the first page.'))

        return mark_safe(u''.join(output))


class DocumentDataGroupForm(forms.Form):
    def __init__(self, *args, **kwargs):
        groups = kwargs.pop('groups', None)
        links = kwargs.pop('links', None)
        current_document = kwargs.pop('current_document', None)
        super(DocumentDataGroupForm, self).__init__(*args, **kwargs)
        for group, data in groups.items():
            self.fields['preview-%s' % group] = forms.CharField(
                widget=DocumentGroupImageWidget(),
                label=u'%s (%d)' % (unicode(data['title']), len(data['documents'])),
                required=False,
                initial={
                    'group': group,
                    'group_data': data['documents'],
                    'current_document': current_document,
                    'links': links
                }
            )
