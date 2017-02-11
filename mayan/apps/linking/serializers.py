from __future__ import absolute_import, unicode_literals

from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import SmartLink, SmartLinkCondition


class SmartLinkConditionSerializer(serializers.HyperlinkedModelSerializer):
    smart_link_url = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'enabled', 'expression', 'foreign_document_data', 'inclusion',
            'id', 'negated', 'operator', 'smart_link_url', 'url'
        )
        model = SmartLinkCondition

    def create(self, validated_data):
        validated_data['smart_link'] = self.context['smart_link']
        return super(SmartLinkConditionSerializer, self).create(validated_data)

    def get_smart_link_url(self, instance):
        return reverse(
            'rest_api:smartlink-detail', args=(instance.smart_link.pk,),
            request=self.context['request'], format=self.context['format']
        )

    def get_url(self, instance):
        return reverse(
            'rest_api:smartlinkcondition-detail', args=(
                instance.smart_link.pk, instance.pk,
            ), request=self.context['request'], format=self.context['format']
        )


class SmartLinkSerializer(serializers.HyperlinkedModelSerializer):
    conditions_url = serializers.HyperlinkedIdentityField(
        view_name='rest_api:smartlinkcondition-list'
    )

    class Meta:
        extra_kwargs = {
            'url': {'view_name': 'rest_api:smartlink-detail'},
        }
        fields = (
            'conditions_url', 'dynamic_label', 'enabled', 'label', 'id', 'url'
        )
        model = SmartLink
