from django.db import models

from .classes import ResolvedSmartLink


class SmartLinkManager(models.Manager):
    def get_for(self, document):
        return [ResolvedSmartLink(smart_link=smart_link, queryset=smart_link.get_linked_document_for(document)) for smart_link in self.filter(enabled=True).filter(document_types=document.document_type)]
