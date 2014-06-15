from django.utils.translation import ugettext_lazy as _

PAGE_SIZE_A5 = u'a5'
PAGE_SIZE_A4 = u'a4'
PAGE_SIZE_A3 = u'a3'
PAGE_SIZE_B5 = u'b5'
PAGE_SIZE_B4 = u'b4'
PAGE_SIZE_LETTER = u'letter'
PAGE_SIZE_LEGAL = u'legal'
PAGE_SIZE_LEDGER = u'ledger'

PAGE_SIZE_DIMENSIONS = (
    (PAGE_SIZE_A5, (u'148mm', u'210mm')),
    (PAGE_SIZE_A4, (u'210mm', u'297mm')),
    (PAGE_SIZE_A3, (u'297mm', u'420mm')),
    (PAGE_SIZE_B5, (u'176mm', u'250mm')),
    (PAGE_SIZE_B4, (u'250mm', u'353mm')),
    (PAGE_SIZE_LETTER, (u'8.5in', u'11in')),
    (PAGE_SIZE_LEGAL, (u'8.5in', u'14in')),
    (PAGE_SIZE_LEDGER, (u'11in', u'17in'))
)

PAGE_SIZE_CHOICES = (
    (PAGE_SIZE_A5, _(u'A5')),
    (PAGE_SIZE_A4, _(u'A4')),
    (PAGE_SIZE_A3, _(u'A3')),
    (PAGE_SIZE_B5, _(u'B5')),
    (PAGE_SIZE_B4, _(u'B4')),
    (PAGE_SIZE_LETTER, _(u'Letter')),
    (PAGE_SIZE_LEGAL, _(u'Legal')),
    (PAGE_SIZE_LEDGER, _(u'Ledger'))
)

PAGE_ORIENTATION_PORTRAIT = u'portrait'
PAGE_ORIENTATION_LANDSCAPE = u'landscape'

PAGE_ORIENTATION_CHOICES = (
    (PAGE_ORIENTATION_PORTRAIT, _(u'Portrait')),
    (PAGE_ORIENTATION_LANDSCAPE, _(u'Landscape')),
)
