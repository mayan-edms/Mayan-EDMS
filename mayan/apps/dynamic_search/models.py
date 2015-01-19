from __future__ import unicode_literals

import urllib
import urlparse

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import smart_str, smart_unicode
from django.utils.translation import ugettext as _

from .managers import RecentSearchManager


class RecentSearch(models.Model):
    """
    Keeps a list of the n most recent search keywords for a given user
    """
    user = models.ForeignKey(User, verbose_name=_('User'), editable=True)
    # Setting editable to True to workaround Django REST framework issue
    # 1604 - https://github.com/tomchristie/django-rest-framework/issues/1604
    # Should be fixed by DRF v2.4.4
    # TODO: Fix after upgrade to DRF v2.4.4

    query = models.TextField(verbose_name=_('Query'), editable=False)
    datetime_created = models.DateTimeField(verbose_name=_('Datetime created'), auto_now=True, db_index=True)
    hits = models.IntegerField(verbose_name=_('Hits'), editable=False)

    objects = RecentSearchManager()

    def __unicode__(self):
        # TODO: Fix this hack, store the search model name in the recent search entry
        from .classes import SearchModel
        document_search = SearchModel.get('documents.Document')

        query_dict = urlparse.parse_qs(urllib.unquote_plus(smart_str(self.query)))

        if self.is_advanced():
            # Advanced search
            advanced_string = []
            for key, value in query_dict.items():
                search_field = document_search.get_search_field(key)
                advanced_string.append('%s: %s' % (search_field.label, smart_unicode(' '.join(value))))

            display_string = ', '.join(advanced_string)
        else:
            # Is a simple search
            display_string = smart_unicode(' '.join(query_dict['q']))

        return '%s (%s)' % (display_string, self.hits)

    def save(self, *args, **kwargs):
        super(RecentSearch, self).save(*args, **kwargs)

    def url(self):
        view = 'search:results' if self.is_advanced() else 'search:search'
        return '%s?%s' % (reverse(view), self.query)

    def is_advanced(self):
        return 'q' not in urlparse.parse_qs(self.query)

    class Meta:
        ordering = ('-datetime_created',)
        verbose_name = _('Recent search')
        verbose_name_plural = _('Recent searches')
