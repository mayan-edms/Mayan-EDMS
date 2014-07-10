from __future__ import absolute_import

from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags
from django.utils.http import urlencode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from converter.literals import (DEFAULT_PAGE_NUMBER, DEFAULT_ROTATION,
                                DEFAULT_ZOOM_LEVEL)

from .conf.settings import DISPLAY_SIZE, MULTIPAGE_PREVIEW_SIZE, THUMBNAIL_SIZE


class DocumentPageImageWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)
        zoom = final_attrs.get('zoom', 100)
        rotation = final_attrs.get('rotation', 0)
        if value:
            output = []
            output.append('<div class="full-height scrollable" style="overflow: auto;" >')
            output.append(document_html_widget(value.document, page=value.page_number, zoom=zoom, rotation=rotation, image_class='lazy-load-interactive', nolazyload=False, size=DISPLAY_SIZE))
            output.append('</div>')
            return mark_safe(u''.join(output))
        else:
            return u''


class DocumentPagesCarouselWidget(forms.widgets.Widget):
    """
    Display many small representations of a document pages
    """
    def render(self, name, value, attrs=None):
        output = []
        output.append(u'<div class="carousel-container" style="white-space:nowrap; overflow: auto;">')

        for page in value.pages.all():

            output.append(u'<div style="display: inline-block; margin: 5px 10px 10px 10px;">')
            output.append(u'<div class="tc">%(page_string)s %(page)s</div>' % {'page_string': ugettext(u'Page'), 'page': page.page_number})
            output.append(
                document_html_widget(
                    page.document,
                    click_view='document_display',
                    page=page.page_number,
                    gallery_name='document_pages',
                    fancybox_class='fancybox-noscaling',
                    image_class='lazy-load-carousel',
                    title=ugettext(u'Page %(page_num)d of %(total_pages)d') % {'page_num': page.page_number, 'total_pages': len(value.pages.all())},
                    size=MULTIPAGE_PREVIEW_SIZE,
                )
            )
            output.append(u'<div class="tc">')
            output.append(u'<a class="fancybox-iframe" href="%s">%s%s</a>' % (reverse('document_page_view', args=[page.pk]), '<span class="famfam active famfam-page_white_go"></span>', ugettext(u'Details')))
            output.append(u'</div></div>')

        output.append(u'</div><br />%s%s' % ('<span class="famfam active famfam-page_white_magnify"></span>', ugettext(u'Click on the image for full size preview')))

        return mark_safe(u''.join(output))


def document_thumbnail(document, **kwargs):
    return document_html_widget(document, click_view='document_display', **kwargs)


def document_link(document):
    return mark_safe(u'<a href="%s">%s</a>' % (reverse('document_view_simple', args=[document.pk]), document))


def document_html_widget(document, click_view=None, page=DEFAULT_PAGE_NUMBER, zoom=DEFAULT_ZOOM_LEVEL, rotation=DEFAULT_ROTATION, gallery_name=None, fancybox_class='fancybox', version=None, image_class='lazy-load', title=None, size=THUMBNAIL_SIZE, nolazyload=False):
    result = []

    alt_text = _(u'document page image')

    if not version:
        version = document.latest_version.pk

    query_dict = {
        'page': page,
        'zoom': zoom,
        'rotation': rotation,
        'version': version,
        'size': size,
    }

    if gallery_name:
        gallery_template = u'rel="%s"' % gallery_name
    else:
        gallery_template = u''

    query_string = urlencode(query_dict)

    preview_view = u'%s?%s' % (reverse('document-image', args=[document.pk]), query_string)

    plain_template = []
    plain_template.append(u'<img src="%s" alt="%s" />' % (preview_view, alt_text))

    result.append(u'<div class="tc" id="document-%d-%d">' % (document.pk, page if page else 1))

    if title:
        title_template = u'title="%s"' % strip_tags(title)
    else:
        title_template = u''

    if click_view:
        result.append(u'<a %s class="%s" href="%s" %s>' % (gallery_template, fancybox_class, u'%s?%s' % (reverse(click_view, args=[document.pk]), query_string), title_template))

    if nolazyload:
        result.append(u'<img style="border: 1px solid black;" src="%s" alt="%s" />' % (preview_view, alt_text))
    else:
        result.append(u'<img class="thin_border %s" data-original="%s" src="%simages/ajax-loader.gif" alt="%s" />' % (image_class, preview_view, settings.STATIC_URL, alt_text))
        result.append(u'<noscript><img style="border: 1px solid black;" src="%s" alt="%s" /></noscript>' % (preview_view, alt_text))

    if click_view:
        result.append(u'</a>')
    result.append(u'</div>')

    return mark_safe(u''.join(result))
