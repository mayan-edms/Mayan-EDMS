from __future__ import unicode_literals

from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse

from mayan.apps.documents.models import DocumentType
from mayan.apps.documents.serializers import DocumentTypeSerializer
from mayan.apps.rest_api.relations import (
    FilteredPrimaryKeyRelatedField, MultiKwargHyperlinkedIdentityField
)
from mayan.apps.user_management.serializers import UserSerializer

from .models import ControlSheet, ControlSheetCode


class ControlSheetSerializer(serializers.HyperlinkedModelSerializer):
    #states = ControlSheetStateSerializer(many=True, required=False)
    #transitions = ControlSheetTransitionSerializer(many=True, required=False)

    code_list_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='control_sheet_id',
        view_name='rest_api:controlsheet-code-list'
    )

    class Meta:
        extra_kwargs = {
            'url': {
                'lookup_url_kwarg': 'control_sheet_id',
                'view_name': 'rest_api:controlsheet-detail'
            },
        }
        fields = ('code_list_url', 'id', 'label', 'url')
        model = ControlSheet


class ControlSheetCodeSerializer(serializers.HyperlinkedModelSerializer):
    control_sheet = ControlSheetSerializer(read_only=True)
    image_url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'control_sheet_id',
                'lookup_url_kwarg': 'control_sheet_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'control_sheet_code_id',
            }
        ),
        view_name='rest_api:controlsheet-code-image'
    )
    url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'control_sheet_id',
                'lookup_url_kwarg': 'control_sheet_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'control_sheet_code_id',
            }
        ),
        view_name='rest_api:controlsheet-code-detail'
    )

    class Meta:
        fields = (
            'arguments', 'control_sheet', 'id', 'image_url', 'name',
            'order', 'url'
        )
        model = ControlSheetCode

    def create(self, validated_data):
        validated_data['control_sheet'] = self.context['control_sheet']
        return super(ControlSheetCodeSerializer, self).create(validated_data)

