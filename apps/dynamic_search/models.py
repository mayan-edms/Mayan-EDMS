import urlparse

from datetime import datetime

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from dynamic_search.managers import RecentSearchManager
from dynamic_search.api import registered_search_dict


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
        query_dict = urlparse.parse_qs(self.query)
        if 'q' in query_dict:
            # Is a simple search
            display_string = u' '.join(query_dict['q'])
        else:
            # Advanced search
            advanced_string = []
            for key, value in query_dict.items():
                # Get model name
                model, field_name = key.split('__', 1)
                model_entry = registered_search_dict.get(model, {})
                if model_entry:
                    # Find the field name title
                    for model_field in model_entry.get('fields', [{}]):
                        if model_field.get('name') == field_name:
                            advanced_string.append(u'%s: %s' % (model_field.get('title', model_field['name']), u' '.join(value)))

            display_string = u', '.join(advanced_string)
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
