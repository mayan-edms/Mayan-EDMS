from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
#from django.shortcuts import get_object_or_404
#from django.utils.translation import ugettext
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse


from permissions.models import Permission


class AccessEntryManager(models.Manager):
	def grant(self, permission, requester, obj):
		"""
		Grant a permission (what), (to) a requester, (on) a specific object
		"""
		access_entry, created = AccessEntry.objects.get_or_create(
			permission=permission,
			holder_type=ContentType.objects.get_for_model(requester),
			holder_id=requester.pk,
			content_type=ContentType.objects.get_for_model(obj),
			object_id=obj.pk
		)
		return created

	def revoke(self, permission, holder, obj):
		try:
			access_entry = AccessEntry.objects.get(
				permission=permission,
				holder_type=ContentType.objects.get_for_model(holder),
				holder_id=holder.pk,
				content_type=ContentType.objects.get_for_model(obj),
				object_id=obj.pk
			)
			access_entry.delete()
			return True
		except AccessEntry.DoesNotExist:
			return False		

	def check_accesses(self, permission_list, requester, obj):
		for permission_item in permission_list:
			permission = get_object_or_404(Permission,
				namespace=permission_item['namespace'], name=permission_item['name'])
			try:
				access_entry = AccessEntry.objects.get(
					permission=permission,
					holder_type=ContentType.objects.get_for_model(requester),
					holder_id=requester.pk,
					content_type=ContentType.objects.get_for_model(obj),
					object_id=obj.pk
				)
				return True
			except AccessEntry.DoesNotExist:
				raise PermissionDenied(ugettext(u'Insufficient permissions.'))
				
	def get_acl_url(self, obj):
		content_type = ContentType.objects.get_for_model(obj.__class__)
		return reverse('acl_list', args=[content_type.app_label, content_type.model, obj.pk])	


class AccessEntry(models.Model):
	permission = models.ForeignKey(Permission, verbose_name=_(u'permission'))
	holder_type = models.ForeignKey(ContentType,
		related_name='access_holder',
		limit_choices_to={'model__in': ('user', 'group', 'role')})
	holder_id = models.PositiveIntegerField()
	holder_object = generic.GenericForeignKey(ct_field='holder_type', fk_field='holder_id')

	content_type = models.ForeignKey(ContentType,
		related_name='object_content_type')
	object_id = models.PositiveIntegerField()
	content_object = generic.GenericForeignKey(ct_field='content_type', fk_field='object_id')

	objects = AccessEntryManager()

	class Meta:
		verbose_name = _(u'access entry')
		verbose_name_plural = _(u'access entries')

	def __unicode__(self):
		return u'%s: %s' % (self.content_type, self.content_object)
