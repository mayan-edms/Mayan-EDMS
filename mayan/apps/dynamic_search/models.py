from __future__ import unicode_literals

import urllib
import urlparse

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import (
    python_2_unicode_compatible, smart_str, smart_unicode
)
from django.utils.translation import ugettext_lazy as _

from .managers import RecentSearchManager


@python_2_unicode_compatible
class RecentSearch(models.Model):
    """
    Keeps a list of the [n] most recent search keywords for a given user
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, editable=False, verbose_name=_('User')
    )
    query = models.TextField(editable=False, verbose_name=_('Query'))
    datetime_created = models.DateTimeField(
        auto_now=True, db_index=True, verbose_name=_('Datetime created')
    )
    hits = models.IntegerField(editable=False, verbose_name=_('Hits'))

    objects = RecentSearchManager()

    def __str__(self):
        # TODO: Fix this hack, store the search model name in the recent
        # search entry
        from .classes import SearchModel
        document_search = SearchModel.get('documents.Document')

        query_dict = urlparse.parse_qs(
            urllib.unquote_plus(smart_str(self.query))
        )

        if self.is_advanced():
            # Advanced search
            advanced_string = []
            for key, value in query_dict.items():
                search_field = document_search.get_search_field(key)
                advanced_string.append(
                    '%s: %s' % (
                        search_field.label, smart_unicode(' '.join(value))
                    )
                )

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
