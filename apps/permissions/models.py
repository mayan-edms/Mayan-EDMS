from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User, Group


class PermissionManager(models.Manager):
    def get_for_holder(self, holder):
        ct = ContentType.objects.get_for_model(holder)
        return [Permission.objects.get(pk=pk) for pk in PermissionHolder.objects.filter(holder_type=ct, holder_id=holder.pk).values_list('permission_id', flat=True)]


class Permission(models.Model):
    namespace = models.CharField(max_length=64, verbose_name=_(u'namespace'))
    name = models.CharField(max_length=64, verbose_name=_(u'name'))
    label = models.CharField(max_length=96, verbose_name=_(u'label'))

    objects = PermissionManager()

    class Meta:
        ordering = ('namespace', 'label')
        unique_together = ('namespace', 'name')
        verbose_name = _(u'permission')
        verbose_name_plural = _(u'permissions')

    def __unicode__(self):
        return self.label
        
    def get_holders(self):
        return [holder.holder_object for holder in self.permissionholder_set.all()]
        
    def has_permission(self, requester):
        if isinstance(requester, User):
            if requester.is_superuser or requester.is_staff:
                return True

        # Request is one of the permission's holders?
        if requester in self.get_holders():
            return True
        
        # If not check if the requesters memberships objects is one of 
        # the permission's holder?
        roles = RoleMember.objects.get_roles_for_member(requester)

        if isinstance(requester, User):
            groups = requester.groups.all()
        else:
            groups = []
            
        for membership in list(set(roles) | set(groups)):
            if self.has_permission(membership):
                return True


class PermissionHolder(models.Model):
    permission = models.ForeignKey(Permission, verbose_name=_(u'permission'))
    holder_type = models.ForeignKey(ContentType,
        related_name='permission_holder',
        limit_choices_to={'model__in': ('user', 'group', 'role')})
    holder_id = models.PositiveIntegerField()
    holder_object = generic.GenericForeignKey(ct_field='holder_type', fk_field='holder_id')

    class Meta:
        verbose_name = _(u'permission holder')
        verbose_name_plural = _(u'permission holders')

    def __unicode__(self):
        return u'%s: %s' % (self.holder_type, self.holder_object)


class Role(models.Model):
    name = models.CharField(max_length=64, unique=True)
    label = models.CharField(max_length=64, unique=True, verbose_name=_(u'label'))

    class Meta:
        ordering = ('label',)
        verbose_name = _(u'role')
        verbose_name_plural = _(u'roles')

    def add_member(self, member):
        role_member, created = RoleMember.objects.get_or_create(
            role=self,
            member_type=ContentType.objects.get_for_model(member),
            member_id=member.pk)

    def __unicode__(self):
        return self.label

    @models.permalink
    def get_absolute_url(self):
        return ('role_list',)


class RoleMemberManager(models.Manager):
    def get_roles_for_member(self, member_obj):
        member_type = ContentType.objects.get_for_model(member_obj)
        return [role_member.role for role_member in RoleMember.objects.filter(member_type=member_type, member_id=member_obj.pk)]


class RoleMember(models.Model):
    role = models.ForeignKey(Role, verbose_name=_(u'role'))
    member_type = models.ForeignKey(ContentType,
        related_name='role_member',
        limit_choices_to={'model__in': ('user', 'group')})
    member_id = models.PositiveIntegerField()
    member_object = generic.GenericForeignKey(ct_field='member_type', fk_field='member_id')

    objects = RoleMemberManager()

    class Meta:
        #ordering = ('label',)
        verbose_name = _(u'role member')
        verbose_name_plural = _(u'role members')

    def __unicode__(self):
        return unicode(self.member_object)
