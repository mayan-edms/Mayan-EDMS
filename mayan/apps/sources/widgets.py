from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.encoding import force_unicode
from django.utils.html import strip_tags
from django.utils.http import urlencode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from converter.literals import DEFAULT_PAGE_NUMBER, DEFAULT_ROTATION, DEFAULT_ZOOM_LEVEL
from documents.conf.settings import THUMBNAIL_SIZE, PREVIEW_SIZE


class FamFamRadioFieldRenderer(forms.widgets.RadioFieldRenderer):
    def render(self):
        results = []
        results.append(u'<ul>\n')
        for w in self:
            if w.choice_value:
                famfam_template = u'<span class="famfam active famfam-%s" style="vertical-align: bottom;"></span>' % w.choice_value
            else:
                famfam_template = u'<span class="famfam active famfam-cross" style="vertical-align: bottom;"></span>'
            results.append(u'<li class="undecorated_list">%s%s</li>' % (famfam_template, force_unicode(w)))

        results.append(u'\n</ul>')
        return mark_safe(u'\n'.join(results))


class FamFamRadioSelect(forms.widgets.RadioSelect):
    renderer = FamFamRadioFieldRenderer


def staging_file_thumbnail(staging_file, **kwargs):
    return staging_file_html_widget(staging_file, click_view='stagingfolderfile-image-view', **kwargs)


def staging_file_html_widget(staging_file, click_view=None, page=DEFAULT_PAGE_NUMBER, zoom=DEFAULT_ZOOM_LEVEL, rotation=DEFAULT_ROTATION, gallery_name=None, fancybox_class='fancybox-staging', image_class='lazy-load', title=None, size=THUMBNAIL_SIZE, nolazyload=False):
    result = []

    alt_text = _(u'staging file page image')

    query_dict = {
        'page': page,
        'zoom': zoom,
        'rotation': rotation,
        'size': size,
    }

    if gallery_name:
        gallery_template = u'rel="%s"' % gallery_name
    else:
        gallery_template = u''

    query_string = urlencode(query_dict)

    preview_view = u'%s?%s' % (reverse('stagingfolderfile-image-view', args=[staging_file.staging_folder.pk, staging_file.encoded_filename]), query_string)

    plain_template = []
    plain_template.append(u'<img src="%s" alt="%s" />' % (preview_view, alt_text))

    result.append(u'<div class="tc" id="staging_file-%s-%d">' % (staging_file.filename, page if page else DEFAULT_PAGE_NUMBER))

    if title:
        title_template = u'title="%s"' % strip_tags(title)
    else:
        title_template = u''

    if click_view:
        # TODO: fix this hack
        query_dict['size'] = PREVIEW_SIZE
        query_string = urlencode(query_dict)
        result.append(u'<a %s class="%s" href="%s" %s>' % (gallery_template, fancybox_class, u'%s?%s' % (reverse(click_view, args=[staging_file.staging_folder.pk, staging_file.encoded_filename]), query_string), title_template))

    if nolazyload:
        result.append(u'<img style="border: 1px solid black;" src="%s" alt="%s" />' % (preview_view, alt_text))
    else:
        result.append(u'<img class="thin_border %s" data-original="%s" src="%simages/ajax-loader.gif" alt="%s" />' % (image_class, preview_view, settings.STATIC_URL, alt_text))
        result.append(u'<noscript><img style="border: 1px solid black;" src="%s" alt="%s" /></noscript>' % (preview_view, alt_text))

    if click_view:
        result.append(u'</a>')
    result.append(u'</div>')

    return mark_safe(u''.join(result))
