from django.utils.translation import ugettext_lazy as _

PAGE_ORIENTATION_PORTRAIT = u'portrait'
PAGE_ORIENTATION_LANDSCAPE = u'landscape'

PAGE_ORIENTATION_CHOICES = (
    (PAGE_ORIENTATION_PORTRAIT, _(u'Portrait')),
    (PAGE_ORIENTATION_LANDSCAPE, _(u'Landscape')),
)
