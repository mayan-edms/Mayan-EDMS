from __future__ import absolute_import

import urlparse
import urllib
import datetime

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_unicode, smart_str
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.simplejson import loads

from .managers import RecentSearchManager, IndexableObjectManager
from .api import registered_search_dict


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
        if self.is_advanced():
            return u'%s (%s)' % (self.get_query(), self.hits)
        else:
            return u'%s (%s)' % (self.get_query().get('q'), self.hits)

    def save(self, *args, **kwargs):
        self.datetime_created = datetime.datetime.now()
        super(RecentSearch, self).save(*args, **kwargs)

    #def readable_query(self):
    #    return self.

    #def url(self):
    #    view = 'results' if self.is_advanced() else 'search'
    #    return '%s?%s' % (reverse(view), self.query)

    def get_query(self):
        return loads(self.query)

    def is_advanced(self):
        return 'q' not in self.get_query()

    class Meta:
        ordering = ('-datetime_created',)
        verbose_name = _(u'recent search')
        verbose_name_plural = _(u'recent searches')


class IndexableObject(models.Model):
    """
    Store a list of object links that have been modified and are 
    meant to be indexed in the next search index update 
    """
    datetime = models.DateTimeField(verbose_name=_(u'date time'))
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    objects = IndexableObjectManager()
    
    def __unicode__(self):
        return unicode(self.content_object)

    def save(self, *args, **kwargs):
        self.datetime = datetime.datetime.now()
        super(IndexableObject, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _(u'indexable object')
        verbose_name_plural = _(u'indexable objects')
