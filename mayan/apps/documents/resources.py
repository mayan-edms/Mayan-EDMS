from __future__ import absolute_import

from django.core.urlresolvers import reverse

from rest_framework import serializers

from .models import Document


class ResourceDocument(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Document
        fields = ('url', 'document_type', 'uuid', 'date_added', 'description')
