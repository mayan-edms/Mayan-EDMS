from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.reverse import reverse

from mayan.apps.django_gpg.models import Key
from mayan.apps.django_gpg.permissions import permission_key_sign
from mayan.apps.rest_api.relations import (
    FilteredPrimaryKeyRelatedField, MultiKwargHyperlinkedIdentityField
)

from .models import DetachedSignature, EmbeddedSignature


class BaseSignatureSerializer(serializers.HyperlinkedModelSerializer):
    document_file_url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'document_file_id',
                'lookup_url_kwarg': 'document_file_id',
            },
            {
                'lookup_field': 'document_file.document_id',
                'lookup_url_kwarg': 'document_id',
            }
        ),
        view_name='rest_api:documentfile-detail'
    )
    key_url = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'date_time', 'document_file_url', 'key_algorithm',
            'key_creation_date', 'key_expiration_date', 'key_id',
            'key_length', 'key_type', 'key_user_id', 'key_url',
            'public_key_fingerprint', 'signature_id', 'url'
        )
        read_only_fields = (
            'date_time', 'document_file_url', 'key_algorithm',
            'key_creation_date', 'key_expiration_date', 'key_id',
            'key_length', 'key_type', 'key_user_id', 'key_url',
            'public_key_fingerprint', 'signature_id', 'url'
        )

    def get_key_url(self, instance):
        key = instance.key

        if key:
            return reverse(
                viewname='rest_api:key-detail', kwargs={
                    'key_id': key.pk
                }, request=self.context['request'],
                format=self.context['format']
            )


class BaseSignSerializer(serializers.HyperlinkedModelSerializer):
    key = FilteredPrimaryKeyRelatedField(
        help_text=_(
            'Primary key of the tag to add to the document.'
        ), source_queryset=Key.objects.private_keys(),
        source_permission=permission_key_sign
    )
    passphrase = serializers.CharField(
        help_text=_(
            'The passphrase to unlock the key and allow it to be used to '
            'sign the document file.'
        ),
        required=False, write_only=True
    )

    class Meta:
        fields = ('key', 'passphrase',)


class DetachedSignatureSerializer(BaseSignatureSerializer):
    url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'document_file.document_id',
                'lookup_url_kwarg': 'document_id',
            },
            {
                'lookup_field': 'document_file_id',
                'lookup_url_kwarg': 'document_file_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'detached_signature_id',
            },
        ),
        view_name='rest_api:detachedsignature-detail'
    )

    class Meta(BaseSignatureSerializer.Meta):
        model = DetachedSignature


class DetachedSignatureUploadSerializer(DetachedSignatureSerializer):
    class Meta(DetachedSignatureSerializer.Meta):
        fields = DetachedSignatureSerializer.Meta.fields + ('signature_file',)
        model = DetachedSignature


class EmbeddedSignatureSerializer(
    BaseSignatureSerializer, serializers.HyperlinkedModelSerializer
):
    url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'document_file.document.pk',
                'lookup_url_kwarg': 'document_id',
            },
            {
                'lookup_field': 'document_file_id',
                'lookup_url_kwarg': 'document_file_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'embedded_signature_id',
            },
        ),
        view_name='rest_api:embeddedsignature-detail'
    )

    class Meta(BaseSignatureSerializer.Meta):
        model = EmbeddedSignature


class SignDetachedSerializer(BaseSignSerializer, BaseSignatureSerializer):
    class Meta(BaseSignSerializer.Meta, BaseSignatureSerializer.Meta):
        model = DetachedSignature


class SignEmbeddedSerializer(SignDetachedSerializer):
    class Meta(SignDetachedSerializer.Meta):
        model = EmbeddedSignature
