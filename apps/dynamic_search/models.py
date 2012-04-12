from __future__ import absolute_import

import urlparse
import urllib
import datetime

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_unicode, smart_str
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from .managers import RecentSearchManager
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
        query_dict = urlparse.parse_qs(urllib.unquote_plus(smart_str(self.query)))
        if 'q' in query_dict:
            # Is a simple search
            display_string = smart_unicode(' '.join(query_dict['q']))
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
                            advanced_string.append(u'%s: %s' % (model_field.get('title', model_field['name']), smart_unicode(' '.join(value))))

            display_string = u', '.join(advanced_string)
        return u'%s (%s)' % (display_string, self.hits)

    def save(self, *args, **kwargs):
        self.datetime_created = datetime.datetime.now()
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


class IndexableObjectManager(models.Manager):
    def get_dirty(self, datetime=None):
        if datetime:
            return self.model.objects.filter(datetime__gte=datetime)
        else:
            return self.model.objects.all()
            
    def get_dirty_pk_list(self, datetime=None):
        return self.get_dirty(datetime).values_list('object_id', flat=True)

    def mark_dirty(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        self.model.objects.get_or_create(content_type=content_type, object_id=obj.pk)
        
    def clear_all(self):
        self.model.objects.all().delete()


class IndexableObject(models.Model):
    """
    Store a list of object links that have been modified and are 
    meant to be indexed in the next search index update 
    """
    datetime = models.DateTimeField(verbose_name=_(u'date time'))
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
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
