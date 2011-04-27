from django.db import models
from django.utils.translation import ugettext as _

from taggit.models import Tag

COLOR_RED = u'red'
COLOR_BLUE = u'blu'
COLOR_MAGENTA = u'mag'
COLOR_CYAN = u'cya'
COLOR_YELLOW = u'yel'

COLOR_CHOICES = (
    (COLOR_RED, _(u'red')),
    (COLOR_BLUE, _(u'blue')),
#    (COLOR_MAGENTA, _(u'magenta')),
#    (COLOR_CYAN, _(u'cyan')),
    (COLOR_YELLOW, _(u'yellow'))
)

COLOR_CODES = (
    (COLOR_RED, u'FF0000'),
    (COLOR_BLUE, u'0000FF'),
#    (COLOR_MAGENTA, u'FF0000'),
#    (COLOR_CYAN, u'FF0000'),
    (COLOR_YELLOW, u'00FFFF')
)
    

class TagProperties(models.Model):
    tag = models.ForeignKey(Tag, verbose_name=_(u'tag'))
    color = models.CharField(max_length=3, choices=COLOR_CHOICES, verbose_name=_(u'color'))

    class Meta:
        verbose_name = _(u'tag properties')
        verbose_name_plural = _(u'tags properties')

    def __unicode__(self):
        return self.tag
