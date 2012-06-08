from __future__ import absolute_import

import logging

from django.contrib.contenttypes.models import ContentType
from django.db.models.base import ModelBase
from django.template.defaultfilters import capfirst
from django.core.exceptions import ObjectDoesNotExist

from common.models import AnonymousUserSingleton

logger = logging.getLogger(__name__)

_cache = {}


def get_source_object(obj):
    try:
        return obj.source_object
    except AttributeError:
        return obj


class EncapsulatedObject(object):
    source_object_name = u'source_object'

    @classmethod
    def object_key(cls, app_label=None, model=None, pk=None):
        if pk:
            return '%s.%s.%s.%s' % (cls.__name__, app_label, model, pk)
        else:
            return '%s.%s.%s' % (cls.__name__, app_label, model)

    @classmethod
    def add_to_class(cls, name, value):
        if hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)

    @classmethod
    def set_source_object_name(cls, new_name):
        cls.source_object_name = new_name

    #@classmethod
    #def encapsulate_list(cls, source_object=None, app_label=None, model=None, pk=None):

    @classmethod
    def encapsulate(cls, source_object):
        source_object = AnonymousUserSingleton.objects.passthru_check(source_object)
        content_type = ContentType.objects.get_for_model(source_object)

        if hasattr(source_object, 'pk'):
            # Object
            object_key = cls.object_key(content_type.app_label, content_type.model, source_object.pk)
        else:
            # Class
            object_key = cls.object_key(content_type.app_label, content_type.model)

        try:
            return _cache[object_key]
        except KeyError:
            encapsulated_object = cls(source_object)
            _cache[object_key] = encapsulated_object
            return encapsulated_object

    @classmethod
    def get(cls, gid):
        elements = gid.split('.')
        if len(elements) == 3:
            app_label, model, pk = elements[0], elements[1], elements[2]
        elif len(elements) == 2:
            app_label, model = elements[0], elements[1]
            pk = None

        object_key = cls.object_key(*elements)

        try:
            return _cache[object_key]
        except KeyError:
            try:
                content_type = ContentType.objects.get(app_label=app_label, model=model)
            except ContentType.DoesNotExist:
                #cls.add_to_class('DoesNotExist', subclass_exception('DoesNotExist', (ObjectDoesNotExist,), cls.__name__))
                #raise cls.DoesNotExist("%s matching query does not exist." % ContentType._meta.object_name)
                raise ObjectDoesNotExist("%s matching query does not exist." % ContentType._meta.object_name)
            else:
                source_object_model_class = content_type.model_class()
                if pk:
                    try:
                        source_object = content_type.get_object_for_this_type(pk=pk)
                    except source_object_model_class.DoesNotExist:
                        #cls.add_to_class('DoesNotExist', subclass_exception('DoesNotExist', (ObjectDoesNotExist,), cls.__name__))
                        #raise cls.DoesNotExist("%s matching query does not exist." % source_object_model_class._meta.object_name)
                        raise ObjectDoesNotExist("%s matching query does not exist." % source_object_model_class._meta.object_name)
                else:
                    source_object = source_object_model_class

            return cls.encapsulate(source_object)

    def __init__(self, source_object):
        self.content_type = ContentType.objects.get_for_model(source_object)
        self.ct_fullname = '%s.%s' % (self.content_type.app_label, self.content_type.model)

        if isinstance(source_object, ModelBase):
            # Class
            self.gid = '%s.%s' % (self.content_type.app_label, self.content_type.model)
        else:
            # Object
            self.gid = '%s.%s.%s' % (self.content_type.app_label, self.content_type.model, source_object.pk)

        setattr(self, self.__class__.source_object_name, source_object)

    def __unicode__(self):
        if isinstance(self.source_object, ModelBase):
            return capfirst(unicode(self.source_object._meta.verbose_name_plural))
        elif self.ct_fullname == 'auth.user':
            return u'%s %s' % (self.source_object._meta.verbose_name, self.source_object.get_full_name())
        elif self.ct_fullname == 'common.anonymoususersingleton':
            return unicode(self.source_object)
        elif self.ct_fullname == 'acls.creatorsingleton':
            return unicode(self.source_object)
        else:
            return u'%s %s' % (self.source_object._meta.verbose_name, self.source_object)

    def __repr__(self):
        return self.__unicode__()

    @property
    def source_object(self):
        return getattr(self, self.__class__.source_object_name, None)
