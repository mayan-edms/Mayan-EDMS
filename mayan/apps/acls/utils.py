from __future__ import unicode_literals

import logging

from django.contrib.contenttypes.models import ContentType

from common.models import AnonymousUserSingleton

from .classes import get_source_object
from .models import AccessEntry, CreatorSingleton, DefaultAccessEntry

logger = logging.getLogger(__name__)


def apply_default_acls(obj, actor=None):
    logger.debug('actor, init: %s', actor)
    obj = get_source_object(obj)

    if actor:
        actor = AnonymousUserSingleton.objects.passthru_check(actor)

    content_type = ContentType.objects.get_for_model(obj)

    for default_acl in DefaultAccessEntry.objects.filter(content_type=content_type):
        holder = CreatorSingleton.objects.passthru_check(default_acl.holder_object, actor)

        if holder:
            # When the creator is admin
            access_entry = AccessEntry(
                permission=default_acl.permission,
                holder_object=holder,
                content_object=obj,
            )
            access_entry.save()
