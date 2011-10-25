from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse

from permissions.models import Permission

from acls.widgets import object_w_content_type_icon


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
			entry = {
				'object': access_entry.holder_object,
				'label': '%s: %s' % (access_entry.holder_type, access_entry.holder_object),
				'widget': object_w_content_type_icon(access_entry.holder_object),
			}
			if entry not in holder_list:
				holder_list.append(entry)
		
		return holder_list

	def get_acls_for_holder(self, obj, holder):
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
