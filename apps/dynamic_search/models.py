from __future__ import absolute_import

import urlparse
import urllib

from datetime import datetime

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_unicode, smart_str

from .managers import RecentSearchManager
from .classes import SearchModel


class RecentSearch(models.Model):
    """
    Keeps a list of the n most recent search keywords for a given user
    """
    user = models.ForeignKey(User, verbose_name=_(u'user'), editable=False)
    query = models.TextField(verbose_name=_(u'query'), editable=False)
    datetime_created = models.DateTimeField(verbose_name=_(u'datetime created'), editable=False)
    hits = models.IntegerField(verbose_name=_(u'hits'), editable=False)

    objects = RecentSearchManager()

    def __unicode__(self):
        document_search = SearchModel.get('documents.Document')
        
        query_dict = urlparse.parse_qs(urllib.unquote_plus(smart_str(self.query)))

        if self.is_advanced():
            # Advanced search
            advanced_string = []
            for key, value in query_dict.items():
                search_field = document_search.get_search_field(key)
                advanced_string.append(u'%s: %s' % (search_field.label, smart_unicode(' '.join(value))))

            display_string = u', '.join(advanced_string)
        else:
            # Is a simple search
            display_string = smart_unicode(' '.join(query_dict['q']))

        return u'%s (%s)' % (display_string, self.hits)

    def save(self, *args, **kwargs):
        self.datetime_created = datetime.now()
        super(RecentSearch, self).save(*args, **kwargs)

    def url(self):
        view = 'results' if self.is_advanced() else 'search'
        return '%s?%s' % (reverse(view), self.query)

    def is_advanced(self):
        return 'q' not in urlparse.parse_qs(self.query)

    class Meta:
        ordering = ('-datetime_created',)
        verbose_name = _(u'recent search')
        verbose_name_plural = _(u'recent searches')
