from __future__ import absolute_import

from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils.http import urlencode

from converter.literals import (DEFAULT_ZOOM_LEVEL, DEFAULT_ROTATION,
    DEFAULT_PAGE_NUMBER)
from mimetype.api import get_error_icon_url


def document_thumbnail(document):
    return document_html_widget(document, click_view='document_preview')


def document_link(document):
    return mark_safe(u'<a href="%s">%s</a>' % (reverse('document_view_simple', args=[document.pk]), document))


def document_html_widget(document, view='document_thumbnail', click_view=None, page=DEFAULT_PAGE_NUMBER, zoom=DEFAULT_ZOOM_LEVEL, rotation=DEFAULT_ROTATION, gallery_name=None, fancybox_class='fancybox', version=None):
    result = []

    alt_text = _(u'document page image')

    if not version:
        version = document.latest_version.pk

    query_dict = {
        'page': page,
        'zoom': zoom,
        'rotation': rotation,
        'version': version,
    }

    if gallery_name:
        gallery_template = u'rel="%s"' % gallery_name
    else:
        gallery_template = u''

    query_string = urlencode(query_dict)
    preview_view = u'%s?%s' % (reverse(view, args=[document.pk]), query_string)

    plain_template = []
    plain_template.append(u'<img src="%s" alt="%s" />' % (preview_view, alt_text))

    result.append(u'<div class="tc" id="document-%d-%d">' % (document.pk, page if page else 1))

    if click_view:
        result.append(u'<a %s class="%s" href="%s">' % (gallery_template, fancybox_class, u'%s?%s' % (reverse(click_view, args=[document.pk]), query_string)))
    result.append(u'<img class="thin_border lazy-load" data-href="%s" src="%simages/ajax-loader.gif" alt="%s" />' % (preview_view, settings.STATIC_URL, alt_text))
    result.append(u'<noscript><img style="border: 1px solid black;" src="%s" alt="%s" /></noscript>' % (preview_view, alt_text))

    if click_view:
        result.append(u'</a>')
    result.append(u'</div>')

    result.append(u'''
        <script type="text/javascript">
        $(document).ready(function() {
            $.get('%(url)s', function(data) {})
                .success(function(data) {
                    if (!data.result) {
                        $('#document-%(pk)d-%(page)d').html('%(plain_template)s');
                    }
                })
                .error(function(data) {
                    $('#document-%(pk)d-%(page)d').html('<img src="%(error_image)s" />');
                });
        });
        </script>
    ''' % {
            'url': reverse('documents-expensive-is_zoomable', args=[document.pk, version, page]),
            'pk': document.pk,
            'page': page if page else 1,
            'plain_template': mark_safe(u''.join(plain_template)),
            'error_image': u''.join([settings.STATIC_URL, get_error_icon_url()]),
        }
    )

    return mark_safe(u''.join(result))
