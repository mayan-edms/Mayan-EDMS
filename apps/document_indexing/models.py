from django.db import models
from django.utils.translation import ugettext_lazy as _

from document_indexing.conf.settings import AVAILABLE_INDEXING_FUNCTIONS

available_indexing_functions_string = (_(u' Available functions: %s') % u','.join([u'%s()' % name for name, function in AVAILABLE_INDEXING_FUNCTIONS.items()])) if AVAILABLE_INDEXING_FUNCTIONS else u''


class DocumentIndex(models.Model):
    expression = models.CharField(max_length=128,
        verbose_name=_(u'indexing expression'),
        help_text=_(u'Enter a python string expression to be evaluated.  The slash caracter "/" acts as a directory delimiter.%s') % available_indexing_functions_string)
    enabled = models.BooleanField(default=True, verbose_name=_(u'enabled'))

    def __unicode__(self):
        return unicode(self.expression)

    class Meta:
        verbose_name = _(u'metadata index')
        verbose_name_plural = _(u'metadata indexes')
