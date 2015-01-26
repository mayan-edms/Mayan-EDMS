from __future__ import unicode_literals

from django import forms
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags
from django.utils.http import urlencode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from converter.literals import (
    DEFAULT_PAGE_NUMBER, DEFAULT_ROTATION, DEFAULT_ZOOM_LEVEL
)

from .settings import DISPLAY_SIZE, THUMBNAIL_SIZE


class DocumentPageImageWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)
        zoom = final_attrs.get('zoom', 100)
        rotation = final_attrs.get('rotation', 0)
        if value:
            output = []
            output.append('<div class="full-height scrollable mayan-page-wrapper-interactive" data-height-difference=230>')
            output.append(document_html_widget(value.document, page=value.page_number, zoom=zoom, rotation=rotation, image_class='lazy-load-interactive', nolazyload=False, size=DISPLAY_SIZE))
            output.append('</div>')
            return mark_safe(''.join(output))
        else:
            return ''


class DocumentPagesCarouselWidget(forms.widgets.Widget):
    """
    Display many small representations of a document pages
    """
    def render(self, name, value, attrs=None):
        output = []
        output.append('<div id="carousel-container" class="full-height scrollable" data-height-difference=360>')

        try:
            document_pages = value.pages.all()
        except AttributeError:
            document_pages = []

        # Reuse expensive values
        latest_version_pk = value.latest_version.pk

        for page in document_pages:
            output.append('<div class="carousel-item">')
            output.append(
                document_html_widget(
                    page.document,
                    click_view='documents:document_page_view',
                    click_view_arguments=[page.pk],
                    page=page.page_number,
                    fancybox_class='fancybox-iframe',
                    image_class='lazy-load-carousel',
                    size=DISPLAY_SIZE,
                    version=latest_version_pk,
                    post_load_class='lazy-load-carousel-loaded',
                )
            )
            output.append('<div class="carousel-item-page-number">%s</div>' % ugettext('Page %(page_number)d') % {'page_number': page.page_number})
            output.append('</div>')

        output.append('</div>')

        return mark_safe(''.join(output))


def document_thumbnail(document, **kwargs):
    return document_html_widget(document, click_view='documents:document_display', **kwargs)


def document_link(document):
    return mark_safe('<a href="%s">%s</a>' % (document.get_absolute_url(), document))


def document_html_widget(document, click_view=None, click_view_arguments=None, page=DEFAULT_PAGE_NUMBER, zoom=DEFAULT_ZOOM_LEVEL, rotation=DEFAULT_ROTATION, gallery_name=None, fancybox_class='fancybox', version=None, image_class='lazy-load', title=None, size=THUMBNAIL_SIZE, nolazyload=False, post_load_class=None):
    result = []

    alt_text = _('Document page image')

    if not version:
        try:
            version = document.latest_version.pk
        except AttributeError:
            version = None

    query_dict = {
        'page': page,
        'zoom': zoom,
        'rotation': rotation,
        'version': version,
        'size': size,
    }

    if gallery_name:
        gallery_template = 'rel="%s"' % gallery_name
    else:
        gallery_template = ''

    query_string = urlencode(query_dict)

    preview_view = '%s?%s' % (reverse('document-image', args=[document.pk]), query_string)

    result.append('<div class="tc" id="document-%d-%d">' % (document.pk, page if page else 1))

    if title:
        title_template = 'title="%s"' % strip_tags(title)
    else:
        title_template = ''

    if click_view:
        result.append('<a %s class="%s" href="%s" %s>' % (gallery_template, fancybox_class, '%s?%s' % (reverse(click_view, args=click_view_arguments or [document.pk]), query_string), title_template))

    if nolazyload:
        result.append('<img class="img-nolazyload" src="%s" alt="%s" />' % (preview_view, alt_text))
    else:
        result.append('<img class="thin_border %s" data-src="%s" data-post-load-class="%s" src="%s" alt="%s" />' % (image_class, preview_view, post_load_class, static('main/icons/hourglass.png'), alt_text))

    if click_view:
        result.append('</a>')
    result.append('</div>')

    return mark_safe(''.join(result))
