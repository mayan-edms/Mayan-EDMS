from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse

from acls.models import AccessControlList

from .models import Tag
from .permissions import permission_tag_attach


class TagSerializer(serializers.HyperlinkedModelSerializer):
    documents = serializers.HyperlinkedIdentityField(
        view_name='rest_api:tag-document-list'
    )
    documents_count = serializers.SerializerMethodField()

    class Meta:
        extra_kwargs = {
            'url': {'view_name': 'rest_api:tag-detail'},
        }
        fields = (
            'color', 'documents', 'documents_count', 'id', 'label', 'url'
        )
        model = Tag

    def get_documents_count(self, instance):
        return instance.documents.count()


class NewTagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'color', 'label', 'id'
        )
        model = Tag


class NewDocumentTagSerializer(serializers.Serializer):
    tag = serializers.IntegerField(
        help_text=_('Primary key of the tag to be added.')
    )

    def create(self, validated_data):
        try:
            tag = Tag.objects.get(pk=validated_data['tag'])

            AccessControlList.objects.check_access(
                permissions=permission_tag_attach,
                user=self.context['request'].user, obj=tag
            )

            tag.documents.add(validated_data['document'])
        except Exception as exception:
            raise ValidationError(exception)

        return {'tag': tag.pk}


class DocumentTagSerializer(TagSerializer):
    remove = serializers.SerializerMethodField()

    def get_remove(self, instance):
        return reverse(
            'rest_api:document-tag', args=(
                self.context['document'].pk, instance.pk,
            ), request=self.context['request'], format=self.context['format']
        )

    class Meta(TagSerializer.Meta):
        fields = TagSerializer.Meta.fields + ('remove',)
        read_only_fields = TagSerializer.Meta.fields
