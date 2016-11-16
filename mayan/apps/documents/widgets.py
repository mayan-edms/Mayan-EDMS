from __future__ import unicode_literals

from django import forms
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags
from django.utils.http import urlencode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext, ugettext_lazy as _

from .settings import (
    setting_display_size, setting_preview_size, setting_thumbnail_size
)


class DocumentPageImageWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)
        zoom = final_attrs.get('zoom')
        rotation = final_attrs.get('rotation')

        html_widget = InteractiveDocumentPageWidget()

        if value:
            output = []
            output.append(
                '<div class="full-height scrollable '
                'mayan-page-wrapper-interactive" data-height-difference=230>'
            )
            output.append(
                html_widget.render(
                    instance=value, zoom=zoom, rotation=rotation,
                )
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
        html_widget = CarouselDocumentPageThumbnailWidget()

        output = []
        output.append(
            '<div id="carousel-container" class="full-height scrollable" '
            'data-height-difference=200>'
        )

        document_pages = value.pages.all()
        total_pages = value.pages.count()

        for document_page in document_pages:
            output.append('<div class="carousel-item">')
            output.append(
                html_widget.render(instance=document_page)
            )

            output.append(
                '<div class="carousel-item-page-number">%s</div>' % ugettext(
                    'Page %(page_number)d of %(total_pages)d'
                ) % {
                    'page_number': document_page.page_number,
                    'total_pages': total_pages
                }
            )
            output.append('</div>')

        if not total_pages:
            output.append('<p>No pages to display</p>')

        output.append('</div>')

        return mark_safe(''.join(output))


def document_link(document):
    return mark_safe('<a href="%s">%s</a>' % (
        document.get_absolute_url(), document)
    )


class InstanceImageWidget(object):
    alt_text = _('Clickable image')
    click_view_name = None
    click_view_query_dict = {}
    destination_view_name = None
    destination_view_query_dict = {}
    disable_title_link = False
    fancybox_class = 'fancybox'
    gallery_name = None
    # TODO: update this to load a disk template
    invalid_image_template = '<p>Invalid image</p>'
    preview_view_name = None
    preview_query_dict = {}
    image_class = 'lazy-load'
    title = None

    # Click view
    def get_click_view_kwargs(self, instance):
        return {
            'pk': instance.pk
        }

    def get_click_view_query_dict(self, instance):
        return self.click_view_query_dict

    def get_click_view_querystring(self, instance):
        return urlencode(self.get_click_view_query_dict(instance=instance))

    def get_click_view_url(self, instance):
        return '{}?{}'.format(
            reverse(
                viewname=self.click_view_name,
                kwargs=self.get_click_view_kwargs(instance=instance)
            ),
            self.get_click_view_querystring(instance=instance)
        )

    # Destination view
    def get_destination_view_querystring(self, instance):
        return urlencode(self.get_destination_view_query_dict(instance=instance))

    def get_destination_url(self, instance):
        return '{}?{}'.format(
            reverse(
                viewname=self.destination_view_name,
                kwargs=self.get_destination_view_kwargs(instance=instance)
            ),
            self.get_destination_view_querystring(instance=instance)
        )

    def get_destination_view_kwargs(self, instance):
        return {
            'pk': instance.pk
        }

    # Preview view
    def get_preview_view_kwargs(self, instance):
        return {
            'pk': instance.pk
        }

    def get_preview_view_query_dict(self, instance):
        return self.preview_view_query_dict

    def get_preview_view_querystring(self, instance):
        return urlencode(self.get_preview_view_query_dict(instance=instance))

    def get_preview_view_url(self, instance):
        return '{}?{}'.format(
            reverse(
                viewname=self.preview_view_name,
                kwargs=self.get_preview_view_kwargs(instance=instance)
            ),
            self.get_preview_view_querystring(instance=instance)
        )

    def get_title(self, instance):
        return self.title

    def is_valid(self, instance):
        return instance

    def render(self, instance):
        result = []

        result.append('<div class="instance-image-widget">')

        if not self.is_valid(instance=instance):
            result.append(self.invalid_image_template)
        else:
            if self.gallery_name:
                gallery_markup = 'rel="%s"' % self.gallery_name
            else:
                gallery_markup = ''

            if self.click_view_name:
                click_full_url = self.get_click_view_url(instance=instance)

                title = self.get_title(instance=instance)

                if title:
                    if not self.disable_title_link:
                        title_markup = 'data-caption="<a class=\'a-caption\' href=\'{url}\'>{title} <i class=\'fa fa-external-link\'></i></a>"'.format(
                            title=strip_tags(title), url=self.get_destination_url(instance=instance) or '#'
                        )
                    else:
                        title_markup = 'data-caption="{title}"'.format(
                            title=strip_tags(title),
                        )
                else:
                    title_markup = ''

                result.append(
                    '<a {gallery_markup} class="{fancybox_class}" '
                    'href="{click_full_url}" {title_markup}>'.format(
                        gallery_markup=gallery_markup,
                        fancybox_class=self.fancybox_class,
                        click_full_url=click_full_url,
                        title_markup=title_markup
                    )
                )

            result.append(
                '<i class="spinner fa fa-spinner fa-pulse fa-3x fa-fw"></i> '
                '<img class="thin_border {image_class}" '
                'data-url="{preview_full_url}" src="#" '
                'alt="{alt_text}" /> '.format(
                    image_class=self.image_class,
                    preview_full_url=self.get_preview_view_url(instance=instance),
                    alt_text=self.alt_text
                )
            )

            if self.click_view_name:
                result.append('</a>')

        result.append('</div>')

        return mark_safe(''.join(result))


class BaseDocumentThumbnailWidget(InstanceImageWidget):
    alt_text = _('Document page image')
    click_view_name = 'rest_api:documentpage-image'
    click_view_query_dict = {
        'size': setting_preview_size.value
    }
    gallery_name = 'document_list'
    invalid_image_template = """
        <span class="fa-stack fa-lg"><i class="fa fa-file-o fa-stack-2x"></i><i class="fa fa-question fa-stack-1x text-danger"></i></span>
    """
    preview_view_name = 'rest_api:documentpage-image'
    preview_view_query_dict = {
        'size': setting_thumbnail_size.value
    }

    def get_destination_url(self, instance):
        return instance.get_absolute_url()


class CarouselDocumentPageThumbnailWidget(BaseDocumentThumbnailWidget):
    click_view_name = 'documents:document_page_view'
    fancybox_class = ''
    image_class = 'lazy-load-carousel'
    preview_view_query_dict = {
        'size': setting_display_size.value
    }


class DocumentThumbnailWidget(BaseDocumentThumbnailWidget):
    def get_click_view_kwargs(self, instance):
        return {
            'pk': instance.latest_version.pages.first().pk
        }

    def get_preview_view_kwargs(self, instance):
        return {
            'pk': instance.latest_version.pages.first().pk
        }

    def get_title(self, instance):
        return getattr(instance, 'label', None)

    def is_valid(self, instance):
        return instance.latest_version.pages.all()


class DocumentPageThumbnailWidget(BaseDocumentThumbnailWidget):
    def get_title(self, instance):
        return unicode(instance)


class InteractiveDocumentPageWidget(BaseDocumentThumbnailWidget):
    click_view_name = None

    def get_preview_view_query_dict(self, instance):
        return {
            'zoom': self.zoom,
            'rotation': self.rotation,
            'size': setting_display_size.value,
        }

    def render(self, instance, *args, **kwargs):
        self.zoom = kwargs.pop('zoom')
        self.rotation = kwargs.pop('rotation')

        return super(
            InteractiveDocumentPageWidget, self
        ).render(instance=instance, *args, **kwargs)
