from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils.http import urlencode

from converter.exceptions import UnknownFileFormat, UnkownConvertError


def document_thumbnail(document):
    return document_html_widget(document, click_view='document_preview')


def document_link(document):
    return mark_safe(u'<a href="%s">%s</a>' % (reverse('document_view_simple', args=[document.pk]), document))


def document_html_widget(document, size='document_thumbnail', click_view=None, page=None, zoom=None, rotation=None, gallery_name=None, fancybox_class='fancybox'):
    result = []
                       
    alt_text = _(u'document page image')
    query_dict = {}
    
    if page:
        query_dict['page'] = page
                       
    if zoom:
        query_dict['zoom'] = zoom

    if rotation:
        query_dict['rotation'] = rotation

    if gallery_name:
        gallery_template = u'rel="%s"' % gallery_name
    else:
        gallery_template = u''
    
    query_string = urlencode(query_dict)
    preview_view = u'%s?%s' % (reverse(size, args=[document.pk]), query_string)

    try:
        document.get_valid_image()
        result.append('<div class="tc">')
        if click_view:
            result.append('<a %s class="%s" href="%s">' % (gallery_template, fancybox_class, u'%s?%s' % (reverse(click_view, args=[document.pk]), query_string)))
        result.append('<img style="border: 1px solid black;" class="lazy-load" data-href="%s" src="%s/images/ajax-loader.gif" alt="%s" />' % (preview_view, settings.STATIC_URL, alt_text))
        result.append('<noscript><img style="border: 1px solid black;" src="%s" alt="%s" /></noscript>' % (preview_view, alt_text))
        if click_view:
            result.append('</a>')
        result.append('</div>')
    except UnknownFileFormat, UnkownConvertError:
        result.append('<div class="tc">')
        result.append('<img class="lazy-load" data-href="%s" src="%s/images/ajax-loader.gif" alt="%s" />' % (preview_view, settings.STATIC_URL, alt_text))
        result.append('<noscript><img src="%s" alt="%s" /></noscript>' % (preview_view, alt_text))
        result.append('</div>')
   
    return mark_safe(u''.join(result))
