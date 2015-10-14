from __future__ import unicode_literals

from django import forms
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags
from django.utils.http import urlencode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from converter.literals import DEFAULT_ROTATION, DEFAULT_ZOOM_LEVEL

from .settings import setting_display_size, setting_thumbnail_size


class DocumentPageImageWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)
        zoom = final_attrs.get('zoom', 100)
        rotation = final_attrs.get('rotation', 0)
        if value:
            output = []
            output.append(
                '<div class="full-height scrollable '
                'mayan-page-wrapper-interactive" data-height-difference=230>'
            )
            output.append(document_html_widget(
                value, zoom=zoom, rotation=rotation, image_class='lazy-load',
                nolazyload=False, size=setting_display_size.value)
            )
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
        output.append(
            '<div id="carousel-container" class="full-height scrollable" '
            'data-height-difference=200>'
        )

        try:
            document_pages = value.pages.all()
            total_pages = value.pages.count()
        except AttributeError:
            document_pages = []
            total_pages = 0

        for page in document_pages:
            output.append('<div class="carousel-item">')
            output.append(
                document_html_widget(
                    page,
                    click_view='documents:document_page_view',
                    click_view_arguments=[page.pk],
                    fancybox_class='',
                    image_class='lazy-load-carousel',
                    size=setting_display_size.value,
                    post_load_class='lazy-load-carousel-loaded',
                )
            )
            output.append(
                '<div class="carousel-item-page-number">%s</div>' % ugettext(
                    'Page %(page_number)d of %(total_pages)d'
                ) % {
                    'page_number': page.page_number,
                    'total_pages': total_pages
                }
            )
            output.append('</div>')

        output.append('</div>')

        return mark_safe(''.join(output))


def document_thumbnail(document, **kwargs):
    return document_html_widget(
        document.latest_version.pages.first(),
        click_view='documents:document_display', **kwargs
    )


def document_link(document):
    return mark_safe('<a href="%s">%s</a>' % (
        document.get_absolute_url(), document)
    )


def document_html_widget(document_page, click_view=None, click_view_arguments=None, zoom=DEFAULT_ZOOM_LEVEL, rotation=DEFAULT_ROTATION, gallery_name=None, fancybox_class='fancybox', image_class='lazy-load', title=None, size=setting_thumbnail_size.value, nolazyload=False, post_load_class=None, disable_title_link=False):
    result = []

    alt_text = _('Document page image')

    if not document_page:
        return mark_safe(
            '<span class="fa-stack fa-lg"><i class="fa fa-file-o fa-stack-2x"></i><i class="fa fa-question fa-stack-1x text-danger"></i></span>'
        )

    document = document_page.document

    query_dict = {
        'zoom': zoom,
        'rotation': rotation,
        'size': size,
    }

    if gallery_name:
        gallery_template = 'rel="%s"' % gallery_name
    else:
        gallery_template = ''

    query_string = urlencode(query_dict)

    preview_view = '%s?%s' % (
        reverse('rest_api:documentpage-image', args=(document_page.pk,)),
        query_string
    )

    result.append(
        '<div class="tc" id="document-%d-%d">' % (
            document.pk, document_page.page_number if document_page.page_number else 1
        )
    )

    if title:
        if not disable_title_link:
            preview_click_link = document.get_absolute_url()
            title_template = 'data-caption="<a class=\'a-caption\' href=\'{url}\'>{title}</a>"'.format(
                title=strip_tags(title), url=preview_click_link or '#'
            )
        else:
            title_template = 'data-caption="{title}"'.format(
                title=strip_tags(title),
            )
    else:
        title_template = ''

    if click_view:
        result.append(
            '<a {gallery_template} class="{fancybox_class}" '
            'href="{image_data}" {title_template}>'.format(
                gallery_template=gallery_template,
                fancybox_class=fancybox_class,
                image_data='%s?%s' % (
                    reverse(
                        click_view, args=click_view_arguments or [document.pk]
                    ), query_string
                ),
                title_template=title_template
            )
        )

    if nolazyload:
        result.append(
            '<img class="img-nolazyload" src="%s" alt="%s" />' % (
                preview_view, alt_text
            )
        )
    else:
        result.append(
            '<img class="thin_border %s" data-src="%s" '
            'data-post-load-class="%s" src="%s" alt="%s" />' % (
                image_class, preview_view, post_load_class,
                static('appearance/images/loading.png'), alt_text
            )
        )

    if click_view:
        result.append('</a>')
    result.append('</div>')

    return mark_safe(''.join(result))
