from __future__ import absolute_import, unicode_literals

from rest_framework import serializers
from rest_framework.reverse import reverse

from documents.serializers import DocumentSerializer

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


class ResolvedSmartLinkDocumentSerializer(DocumentSerializer):
    resolved_smart_link_url = serializers.SerializerMethodField()

    class Meta(DocumentSerializer.Meta):
        fields = DocumentSerializer.Meta.fields + (
            'resolved_smart_link_url',
        )
        read_only_fields = DocumentSerializer.Meta.fields

    def get_resolved_smart_link_url(self, instance):
        return reverse(
            'rest_api:resolvedsmartlink-detail', args=(
                self.context['document'].pk, self.context['smart_link'].pk
            ), request=self.context['request'],
            format=self.context['format']
        )


class ResolvedSmartLinkSerializer(SmartLinkSerializer):
    resolved_dynamic_label = serializers.SerializerMethodField()
    resolved_smart_link_url = serializers.SerializerMethodField()
    resolved_documents_url = serializers.SerializerMethodField()

    class Meta(SmartLinkSerializer.Meta):
        fields = SmartLinkSerializer.Meta.fields + (
            'resolved_dynamic_label', 'resolved_smart_link_url',
            'resolved_documents_url'
        )
        read_only_fields = SmartLinkSerializer.Meta.fields

    def get_resolved_documents_url(self, instance):
        return reverse(
            'rest_api:resolvedsmartlinkdocument-list',
            args=(self.context['document'].pk, instance.pk,),
            request=self.context['request'], format=self.context['format']
        )

    def get_resolved_dynamic_label(self, instance):
        return instance.get_dynamic_label(document=self.context['document'])

    def get_resolved_smart_link_url(self, instance):
        return reverse(
            'rest_api:resolvedsmartlink-detail',
            args=(self.context['document'].pk, instance.pk,),
            request=self.context['request'], format=self.context['format']
        )


class WritableSmartLinkSerializer(serializers.ModelSerializer):
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
