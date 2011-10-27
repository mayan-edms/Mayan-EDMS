from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from permissions.models import Permission

#from acls.widgets import object_w_content_type_icon

_encapsulation_cache = {}

class EncapsulatedObject(object):
    source_object_name = u'source_object'
    '''
    @classmethod
    def get_by_ct(cls, content_type, object_id):
        """
        Return a single ACLHolder instance corresponding to the content
        type object given as argument
        """
        try:
            return AccessHolder(
                holder_object=ContentType.objects.get(content_type=access_entry.holder_type, object_id=access_entry.holder_id)
            )
        except ContentType.DoesNotExits:
            raise ObjectDoesNotExist
    '''
    @classmethod
    def set_source_object_name(cls, new_name):
        cls.source_object_name = new_name
    
    @classmethod
    def encapsulate(cls, source_object):
        if source_object not in _encapsulation_cache:
            encapsulated_object = cls(source_object)
            _encapsulation_cache[source_object] = encapsulated_object
        else:
            return _encapsulation_cache[source_object]
        return encapsulated_object

    @classmethod
    def get(cls, gid):
        app_label, model, pk = gid.split('.')
        content_type = ContentType.objects.get(app_label=app_label, model=model)
        source_object = content_type.get_object_for_this_type(pk=pk)
        return cls.encapsulate(source_object)
                
    def __init__(self, source_object):
        content_type = ContentType.objects.get_for_model(source_object)
        self.gid = '%s.%s.%s' % (content_type.app_label, content_type.name, source_object.pk)
        #self.source_object_name = self.__class__.source_object_name
        #self.source_object = source_object
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

    def check_accesses(self, permission_list, requester, obj):
        for permission_item in permission_list:
            permission = get_object_or_404(Permission,
                namespace=permission_item['namespace'], name=permission_item['name'])
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
                raise PermissionDenied(ugettext(u'Insufficient permissions.'))
                
    def get_acl_url(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return reverse('acl_list', args=[content_type.app_label, content_type.model, obj.pk])
        
    def get_holders_for(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        holder_list = []
        for access_entry in self.model.objects.filter(content_type=content_type, object_id=obj.pk):
            #entry = {
            #	'object': access_entry.holder_object,
            #	'label': '%s: %s' % (access_entry.holder_type, access_entry.holder_object),
            #	#'widget': object_w_content_type_icon(access_entry.holder_object),
            #    'compound_id': '9',
            #}
            #entry = ACLHolder.objects.get(content_type=access_entry.holder_type, object_id=access_entry.holder_id)
            #entry = access_entry.holder_object
            entry = AccessHolder.encapsulate(access_entry.holder_object)
            
            if entry not in holder_list:
                holder_list.append(entry)
        
        return holder_list

    def get_permissions_for_holder(self, obj, holder):
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
