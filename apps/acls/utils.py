from __future__ import absolute_import

from django.contrib.contenttypes.models import ContentType

from .models import AccessEntry, DefaultAccessEntry, CreatorSingleton
from .classes import EncapsulatedObject, AccessHolder, ClassAccessHolder


def apply_default_acls(self, obj, actor=None):
    if isinstance(obj, EncapsulatedObject):
        obj = obj.source_object

    if actor:
        actor = AnonymousUserSingleton.objects.passthru_check(actor)
        #actor_type = ContentType.objects.get_for_model(actor)

    content_type = ContentType.objects.get_for_model(obj)

    for default_acl in DefaultAccessEntry.objects.filter(content_type=content_type):
        holder = CreatorSingleton.objects.passthru_check(default_acl.holder_object, actor)
        
        access_entry = AccessEntry(
            permission=default_acl.permission,
            holder_object=holder,
            content_object=obj,
        )
        access_entry.save()
