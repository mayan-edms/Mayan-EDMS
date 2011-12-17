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
from django.db.models.base import ModelBase
from django.template.defaultfilters import capfirst

from permissions.models import StoredPermission

_cache = {}

_class_permissions = {}


def class_permissions(cls, permission_list):
    stored_permissions = _class_permissions.setdefault(cls, [])
    stored_permissions.extend(permission_list)
            
            
class EncapsulatedObject(object):
    source_object_name = u'source_object'

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
        elif app_label and model:
            try:
                content_type = ContentType.objects.get(app_label=app_label, model=model)
                source_object_model_class = content_type.model_class()
                if pk:
                    source_object = content_type.get_object_for_this_type(pk=pk)
                else:
                    source_object = source_object_model_class
            except ContentType.DoesNotExist:
                #cls.add_to_class('DoesNotExist', subclass_exception('DoesNotExist', (ObjectDoesNotExist,), cls.__name__))
                #raise cls.DoesNotExist("%s matching query does not exist." % ContentType._meta.object_name)
                raise ObjectDoesNotExist("%s matching query does not exist." % ContentType._meta.object_name)
            except source_object_model_class.DoesNotExist:
                #cls.add_to_class('DoesNotExist', subclass_exception('DoesNotExist', (ObjectDoesNotExist,), cls.__name__))
                #raise cls.DoesNotExist("%s matching query does not exist." % source_object_model_class._meta.object_name)
                raise ObjectDoesNotExist("%s matching query does not exist." % source_object_model_class._meta.object_name)
           
        if hasattr(source_object, 'pk'):
            # Object
            object_key = '%s.%s.%s.%s' % (cls.__name__, content_type.app_label, content_type.model, source_object.pk)
        else:
            # Class
            object_key = '%s.%s.%s' % (cls.__name__, content_type.app_label, content_type.model)

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
            object_key = '%s.%s.%s.%s' % (cls.__name__, app_label, model, pk)
        elif len(elements) == 2:
            app_label, model = elements[0], elements[1]
            pk = None
            object_key = '%s.%s.%s' % (cls.__name__, app_label, model)
            
        try:
            return _cache[object_key]
        except KeyError:
            if pk:
                return cls.encapsulate(app_label=app_label, model=model, pk=pk)
            else:
                return cls.encapsulate(app_label=app_label, model=model)
                
    def __init__(self, source_object):
        self.content_type = ContentType.objects.get_for_model(source_object)
        self.ct_fullname = '%s.%s' % (self.content_type.app_label, self.content_type.name)

        if isinstance(source_object, ModelBase):
            # Class
            self.gid = '%s.%s' % (self.content_type.app_label, self.content_type.name)
        else:
            # Object 
            self.gid = '%s.%s.%s' % (self.content_type.app_label, self.content_type.name, source_object.pk)
            
        setattr(self, self.__class__.source_object_name, source_object)

    def __unicode__(self):
        if isinstance(self.source_object, ModelBase):
            return capfirst(unicode(self.source_object._meta.verbose_name_plural))
            
        elif self.ct_fullname == 'auth.user':
            return u'%s %s' % (self.source_object._meta.verbose_name, self.source_object.get_full_name())
        else:
            #label = unicode(obj)
            return u'%s %s' % (self.source_object._meta.verbose_name, self.source_object)
            
            #return unicode(getattr(self, self.__class__.source_object_name, None))

    def __repr__(self):
        return self.__unicode__()
        
    @property
    def source_object(self):
        return getattr(self, self.__class__.source_object_name, None)
        
    def get_class_permissions(self):
        return _class_permissions.get(self.content_type.model_class(), [])
        
        
class AccessHolder(EncapsulatedObject):
    source_object_name = u'holder_object'
    
    
class AccessObject(EncapsulatedObject):
    source_object_name = u'obj'    
   

class AccessObjectClass(EncapsulatedObject):
    source_object_name = u'cls'


class ClassAccessHolder(EncapsulatedObject):
    source_object_name = u'class_holder'


class AccessEntryManager(models.Manager):
    def grant(self, permission, requester, obj):
        '''
        Grant a permission (what), (to) a requester, (on) a specific object
        '''
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
                permission=permission.get_stored_permission(),
                holder_type=ContentType.objects.get_for_model(requester),
                holder_id=requester.pk,
                content_type=ContentType.objects.get_for_model(obj),
                object_id=obj.pk
            )
            return True
        except self.model.DoesNotExist:
            return False
                
    def check_access(self, permission, requester, obj):
        if self.has_accesses(permission, requester, obj):
            return True
        else:
            raise PermissionDenied(ugettext(u'Insufficient permissions.'))
                
    def get_acl_url(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return reverse('acl_list', args=[content_type.app_label, content_type.model, obj.pk])

    def get_new_holder_url(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return reverse('acl_new_holder_for', args=[content_type.app_label, content_type.model, obj.pk])
        
    def get_holders_for(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        holder_list = []
        for access_entry in self.model.objects.filter(content_type=content_type, object_id=obj.pk):
            entry = AccessHolder.encapsulate(access_entry.holder_object)
            
            if entry not in holder_list:
                holder_list.append(entry)
        
        return holder_list

    def get_holder_permissions_for(self, obj, holder):
        if isinstance(holder, User):
            if holder.is_superuser or holder.is_staff:
                return Permission.objects.all()
                        
        holder_type = ContentType.objects.get_for_model(holder)
        content_type = ContentType.objects.get_for_model(obj)
        return [access.permission for access in self.model.objects.filter(content_type=content_type, object_id=obj.pk, holder_type=holder_type, holder_id=holder.pk)]


class AccessEntry(models.Model):
    permission = models.ForeignKey(StoredPermission, verbose_name=_(u'permission'))

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


class DefaultAccessEntryManager(models.Manager):
    def get_holders_for(self, cls):
        if isinstance(cls, EncapsulatedObject):
            cls = cls.source_object

        content_type = ContentType.objects.get_for_model(cls)
        holder_list = []
        for access_entry in self.model.objects.filter(content_type=content_type):
            entry = ClassAccessHolder.encapsulate(access_entry.holder_object)
            
            if entry not in holder_list:
                holder_list.append(entry)
        
        return holder_list

    def has_accesses(self, permission, requester, cls):
        if isinstance(requester, User):
            if requester.is_superuser or requester.is_staff:
                return True
                        
        try:
            access_entry = self.model.objects.get(
                permission=permission.get_stored_permission(),
                holder_type=ContentType.objects.get_for_model(requester),
                holder_id=requester.pk,
                content_type=ContentType.objects.get_for_model(cls),
            )
            return True
        except self.model.DoesNotExist:
            return False

    def grant(self, permission, requester, cls):
        '''
        Grant a permission (what), (to) a requester, (on) a specific class
        '''
        access_entry, created = self.model.objects.get_or_create(
            permission=permission,
            holder_type=ContentType.objects.get_for_model(requester),
            holder_id=requester.pk,
            content_type=ContentType.objects.get_for_model(cls),
        )
        return created

    def revoke(self, permission, holder, cls):
        try:
            access_entry = self.model.objects.get(
                permission=permission,
                holder_type=ContentType.objects.get_for_model(holder),
                holder_id=holder.pk,
                content_type=ContentType.objects.get_for_model(cls),
            )
            access_entry.delete()
            return True
        except self.model.DoesNotExist:
            return False		

    def get_holder_permissions_for(self, cls, holder):
        if isinstance(holder, User):
            if holder.is_superuser or holder.is_staff:
                return Permission.objects.all()
                        
        holder_type = ContentType.objects.get_for_model(holder)
        content_type = ContentType.objects.get_for_model(cls)
        return [access.permission for access in self.model.objects.filter(content_type=content_type, holder_type=holder_type, holder_id=holder.pk)]


class DefaultAccessEntry(models.Model):
    @classmethod
    def get_classes(cls):
        return [AccessObjectClass.encapsulate(cls) for cls in _class_permissions.keys()]

    permission = models.ForeignKey(StoredPermission, verbose_name=_(u'permission'))

    holder_type = models.ForeignKey(
        ContentType,
        limit_choices_to={'model__in': ('user', 'group', 'role')},
        related_name='default_access_entry_holder'
    )
    holder_id = models.PositiveIntegerField()
    holder_object = generic.GenericForeignKey(
        ct_field='holder_type',
        fk_field='holder_id'
    )

    content_type = models.ForeignKey(
        ContentType,
        related_name='default_access_entry_class'
    )

    objects = DefaultAccessEntryManager()

    class Meta:
        verbose_name = _(u'default access entry')
        verbose_name_plural = _(u'default access entries')

    def __unicode__(self):
        return u'%s: %s' % (self.content_type, self.content_object)


if sys.version_info < (2, 5):
    # Prior to Python 2.5, Exception was an old-style class
    def subclass_exception(name, parents, unused):
        return types.ClassType(name, parents, {})
else:
    def subclass_exception(name, parents, module):
        return type(name, parents, {'__module__': module})

