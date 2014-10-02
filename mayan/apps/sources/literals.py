from django.utils.translation import ugettext_lazy as _

SOURCE_UNCOMPRESS_CHOICE_Y = 'y'
SOURCE_UNCOMPRESS_CHOICE_N = 'n'
SOURCE_UNCOMPRESS_CHOICE_ASK = 'a'

SOURCE_UNCOMPRESS_CHOICES = (
    (SOURCE_UNCOMPRESS_CHOICE_Y, _(u'Always')),
    (SOURCE_UNCOMPRESS_CHOICE_N, _(u'Never')),
)

SOURCE_INTERACTIVE_UNCOMPRESS_CHOICES = (
    (SOURCE_UNCOMPRESS_CHOICE_Y, _(u'Always')),
    (SOURCE_UNCOMPRESS_CHOICE_N, _(u'Never')),
    (SOURCE_UNCOMPRESS_CHOICE_ASK, _(u'Ask user'))
)

SOURCE_CHOICE_WEB_FORM = 'webform'
SOURCE_CHOICE_STAGING = 'staging'
SOURCE_CHOICE_WATCH = 'watch'

SOURCE_CHOICES = (
    (SOURCE_CHOICE_WEB_FORM, _(u'Web form')),
    (SOURCE_CHOICE_STAGING, _(u'Server staging folder')),
    (SOURCE_CHOICE_WATCH, _(u'Server watch folder')),
)

SOURCE_CHOICES_PLURAL = (
    (SOURCE_CHOICE_WEB_FORM, _(u'Web forms')),
    (SOURCE_CHOICE_STAGING, _(u'Server staging folders')),
    (SOURCE_CHOICE_WATCH, _(u'Server watch folders')),
)
