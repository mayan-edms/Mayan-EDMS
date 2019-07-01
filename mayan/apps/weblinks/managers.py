from django.db import models

from mayan.apps.acls.models import AccessControlList

from .permissions import permission_web_link_instance_view


class WebLinkManager(models.Manager):
    def get_for(self, document, user):
        queryset = self.filter(
            document_types=document.document_type, enabled=True
        )
        return AccessControlList.objects.restrict_queryset(
            permission=permission_web_link_instance_view,
            queryset=queryset, user=user
        )
