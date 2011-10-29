import sys
import types

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from permissions.models import Permission

_cache = {}


class EncapsulatedObject(object):
    source_object_name = u'source_object'

    #@classmethod
    #def __new__(cls, *args, **kwargs):
    #    cls.add_to_class('DoesNotExist', subclass_exception('DoesNotExist', (ObjectDoesNotExist,), cls.__name__))
    #    return super(EncapsulatedObject, cls).__new__(*args, **kwargs)

    @classmethod
    def add_to_class(cls, name, value):
        if hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else:
           setattr(cls, name, value)

    @classmethod
    def set_source_object_name(cls, new_name):
        cls.source_object_name = new_name
    
    @classmethod
    def encapsulate(cls, source_object=None, app_label=None, model=None, pk=None):
        if source_object:
            content_type = ContentType.objects.get_for_model(source_object)
        elif app_label and model and pk:
            try:
                content_type = ContentType.objects.get(app_label=app_label, model=model)
                source_object_model_class = content_type.model_class()
                source_object = content_type.get_object_for_this_type(pk=pk)
            except ContentType.DoesNotExist:
                #cls.add_to_class('DoesNotExist', subclass_exception('DoesNotExist', (ObjectDoesNotExist,), cls.__name__))
                #raise cls.DoesNotExist("%s matching query does not exist." % ContentType._meta.object_name)
                raise ObjectDoesNotExist("%s matching query does not exist." % ContentType._meta.object_name)
            except source_object_model_class.DoesNotExist:
                #cls.add_to_class('DoesNotExist', subclass_exception('DoesNotExist', (ObjectDoesNotExist,), cls.__name__))
                #raise cls.DoesNotExist("%s matching query does not exist." % source_object_model_class._meta.object_name)
                raise ObjectDoesNotExist("%s matching query does not exist." % source_object_model_class._meta.object_name)
           
        object_key = '%s.%s.%s.%s' % (cls.__name__, content_type.app_label, content_type.model, source_object.pk)

        try:
            return _cache[object_key]
        except KeyError:
            encapsulated_object = cls(source_object)
            _cache[object_key] = encapsulated_object
            return encapsulated_object

    @classmethod
    def get(cls, gid):
        app_label, model, pk = gid.split('.')
        object_key = '%s.%s.%s.%s' % (cls.__name__, app_label, model, pk)
        try:
            return _cache[object_key]
        except KeyError:
            return cls.encapsulate(app_label=app_label, model=model, pk=pk)
                
    def __init__(self, source_object):
        content_type = ContentType.objects.get_for_model(source_object)
        self.gid = '%s.%s.%s' % (content_type.app_label, content_type.name, source_object.pk)
        setattr(self, self.__class__.source_object_name, source_object)

    def __unicode__(self):
        return unicode(getattr(self, self.__class__.source_object_name, None))

    def __repr__(self):
        return self.__unicode__()
        
    @property
    def source_object(self):
        return getattr(self, self.__class__.source_object_name, None)
        
        
class AccessHolder(EncapsulatedObject):
    source_object_name = u'holder_object'
    
    
class AccessObject(EncapsulatedObject):
    source_object_name = u'obj'    
   

class AccessEntryManager(models.Manager):
    def grant(self, permission, requester, obj):
        """
        Grant a permission (what), (to) a requester, (on) a specific object
        """
        access_entry, created = self.model.objects.get_or_create(
            permission=permission,
            holder_type=ContentType.objects.get_for_model(requester),
            holder_id=requester.pk,
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk
        )
        return created

    def revoke(self, permission, holder, obj):
        try:
            access_entry = self.model.objects.get(
                permission=permission,
                holder_type=ContentType.objects.get_for_model(holder),
                holder_id=holder.pk,
                content_type=ContentType.objects.get_for_model(obj),
                object_id=obj.pk
            )
            access_entry.delete()
            return True
        except self.model.DoesNotExist:
            return False		

    def has_accesses(self, permission, requester, obj):
        if isinstance(requester, User):
            if requester.is_superuser or requester.is_staff:
                return True
                        
        try:
            access_entry = self.model.objects.get(
                permission=permission,
                holder_type=ContentType.objects.get_for_model(requester),
                holder_id=requester.pk,
                content_type=ContentType.objects.get_for_model(obj),
                object_id=obj.pk
            )
            return True
        except self.model.DoesNotExist:
            return False
                
    def check_access(self, permission, requester, obj):
        if has_accesses(permission, requester, obj):
            return True
        else:
            raise PermissionDenied(ugettext(u'Insufficient permissions.'))
                
    def get_acl_url(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return reverse('acl_list', args=[content_type.app_label, content_type.model, obj.pk])
        
    def get_holders_for(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        holder_list = []
        for access_entry in self.model.objects.filter(content_type=content_type, object_id=obj.pk):
            entry = AccessHolder.encapsulate(access_entry.holder_object)
            
            if entry not in holder_list:
                holder_list.append(entry)
        
        return holder_list

    def get_permissions_for_holder(self, obj, holder):
        if isinstance(holder, User):
            if holder.is_superuser or holder.is_staff:
                return Permission.objects.active_only()
                        
        holder_type = ContentType.objects.get_for_model(holder)
        content_type = ContentType.objects.get_for_model(obj)
        return [access.permission for access in self.model.objects.filter(content_type=content_type, object_id=obj.pk, holder_type=holder_type, holder_id=holder.pk)]


class AccessEntry(models.Model):
    permission = models.ForeignKey(Permission, verbose_name=_(u'permission'))

    holder_type = models.ForeignKey(
        ContentType,
        related_name='access_holder',
        limit_choices_to={'model__in': ('user', 'group', 'role')}
    )
    holder_id = models.PositiveIntegerField()
    holder_object = generic.GenericForeignKey(
        ct_field='holder_type',
        fk_field='holder_id'
    )

    content_type = models.ForeignKey(
        ContentType,
        related_name='object_content_type'
    )
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey(
        ct_field='content_type',
        fk_field='object_id'
    )

    objects = AccessEntryManager()

    class Meta:
        verbose_name = _(u'access entry')
        verbose_name_plural = _(u'access entries')

    def __unicode__(self):
        return u'%s: %s' % (self.content_type, self.content_object)


if sys.version_info < (2, 5):
    # Prior to Python 2.5, Exception was an old-style class
    def subclass_exception(name, parents, unused):
        return types.ClassType(name, parents, {})
else:
    def subclass_exception(name, parents, module):
        return type(name, parents, {'__module__': module})

