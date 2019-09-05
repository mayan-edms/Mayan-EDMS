from __future__ import unicode_literals

from rest_framework import serializers

from mayan.apps.rest_api.relations import MultiKwargHyperlinkedIdentityField

from .models import ControlSheet, ControlSheetCode


class ControlSheetSerializer(serializers.HyperlinkedModelSerializer):
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
