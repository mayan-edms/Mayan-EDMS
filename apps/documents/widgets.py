from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse


def document_thumbnail(document):
    try:
        return mark_safe(u'<a class="fancybox" href="%(url)s"><img class="lazy-load" data-href="%(thumbnail)s" src="%(static_url)s/images/ajax-loader.gif" alt="%(string)s" /><noscript><img src="%(thumbnail)s" alt="%(string)s" /></noscript></a>' % {
            'url': reverse('document_preview', args=[document.pk]),
            'thumbnail': reverse('document_thumbnail', args=[document.pk]),
            'static_url': settings.STATIC_URL,
            'string': _(u'thumbnail')
        })
    except:
        return u''


def document_link(document):
    return mark_safe(u'<a href="%s">%s</a>' % (reverse('document_view_simple', args=[document.pk]), document))
