from django.db import models
from django.utils.translation import ugettext_lazy as _

from taggit.models import Tag

COLOR_RED = u'red'
COLOR_BLUE = u'blu'
COLOR_MAGENTA = u'mag'
COLOR_CYAN = u'cya'
COLOR_YELLOW = u'yel'
COLOR_GREENYELLOW = u'gry'

COLOR_CHOICES = (
    (COLOR_BLUE, _(u'Blue')),
    (COLOR_CYAN, _(u'Cyan')),
    (COLOR_GREENYELLOW, _(u'Green-Yellow')),
    (COLOR_MAGENTA, _(u'Magenta')),
    (COLOR_RED, _(u'Red')),
    (COLOR_YELLOW, _(u'Yellow'))
)

COLOR_CODES = (
    (COLOR_RED, u'red'),
    (COLOR_BLUE, u'blue'),
    (COLOR_MAGENTA, u'magenta'),
    (COLOR_CYAN, u'cyan'),
    (COLOR_YELLOW, u'yellow'),
    (COLOR_GREENYELLOW, u'greenyellow '),
)
    

class TagProperties(models.Model):
    tag = models.ForeignKey(Tag, verbose_name=_(u'tag'))
    color = models.CharField(max_length=3, choices=COLOR_CHOICES, verbose_name=_(u'color'))

    class Meta:
        verbose_name = _(u'tag properties')
        verbose_name_plural = _(u'tags properties')

    def __unicode__(self):
        return unicode(self.tag)

    def get_color_code(self):
        return dict(COLOR_CODES)[self.color]
