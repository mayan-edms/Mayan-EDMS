from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from mayan.apps.acls.models import AccessControlList
from mayan.apps.django_gpg.models import Key
from mayan.apps.django_gpg.permissions import permission_key_sign
from mayan.apps.rest_api.relations import MultiKwargHyperlinkedIdentityField

from .models import DetachedSignature, EmbeddedSignature


class BaseSignatureSerializer(serializers.HyperlinkedModelSerializer):
    document_version_url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'document_version_id',
                'lookup_url_kwarg': 'version_pk',
            },
            {
                'lookup_field': 'document_version.document.pk',
                'lookup_url_kwarg': 'pk',
            }
        ),
        view_name='rest_api:documentversion-detail'
    )


class BaseSignSerializer(serializers.HyperlinkedModelSerializer):
    passphrase = serializers.CharField(
        help_text=_(
            'The passphrase to unlock the key and allow it to be used to '
            'sign the document version.'
        ),
        required=False, write_only=True
    )


class DetachedSignatureSerializer(BaseSignatureSerializer):
    url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'document_version.document.pk',
                'lookup_url_kwarg': 'document_id',
            },
            {
                'lookup_field': 'document_version_id',
                'lookup_url_kwarg': 'document_version_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'detached_signature_id',
            },
        ),
        view_name='rest_api:detachedsignature-detail'
    )

    class Meta:
        extra_kwargs = {
            'signature_file': {'write_only': True},
        }
        fields = (
            'date', 'document_version_url', 'key_id', 'signature_file',
            'signature_id', 'public_key_fingerprint', 'url'
        )
        model = DetachedSignature
        read_only_fields = ('key_id',)

    def create(self, validated_data):
        validated_data['document_version'] = self.context['document_version']
        return super(DetachedSignatureSerializer, self).create(
            validated_data=validated_data
        )


class EmbeddedSignatureSerializer(serializers.HyperlinkedModelSerializer):
    document_version_url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'document_version_id',
                'lookup_url_kwarg': 'version_pk',
            },
            {
                'lookup_field': 'document_version.document.pk',
                'lookup_url_kwarg': 'pk',
            }
        ),
        view_name='rest_api:documentversion-detail'
    )

    url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'document_version.document.pk',
                'lookup_url_kwarg': 'document_id',
            },
            {
                'lookup_field': 'document_version_id',
                'lookup_url_kwarg': 'document_version_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'embedded_signature_id',
            },
        ),
        view_name='rest_api:embeddedsignature-detail'
    )
    passphrase = serializers.CharField(required=False, write_only=True)

    class Meta:
        fields = (
            'date', 'document_version_url', 'key_id', 'signature_id',
            'passphrase', 'public_key_fingerprint', 'url'
        )
        model = EmbeddedSignature

    def create(self, validated_data):
        key_id = validated_data.pop('key_id')
        passphrase = validated_data.pop('passphrase', None)

        key_queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_key_sign, queryset=Key.objects.all(),
            user=self.context['request'].user
        )

        try:
            key = key_queryset.get(fingerprint__endswith=key_id)
        except Key.DoesNotExist:
            raise ValidationError(
                {
                    'key_id': [
                        'Key "{}" not found.'.format(key_id)
                    ]
                }, code='invalid'
            )

        signature = EmbeddedSignature.objects.sign_document_version(
            document_version=self.context['document_version'], key=key,
            passphrase=passphrase, user=self.context['request'].user
        )

        return signature


class SignDetachedSerializer(BaseSignatureSerializer, BaseSignSerializer):
    class Meta:
        fields = (
            'date', 'document_version_url', 'key_id', 'signature_id',
            'passphrase', 'public_key_fingerprint', 'url'
        )
        model = DetachedSignature

    def sign(self, key_id, passphrase):
        key_queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_key_sign, queryset=Key.objects.all(),
            user=self.context['request'].user
        )

        try:
            key = key_queryset.get(fingerprint__endswith=key_id)
        except Key.DoesNotExist:
            raise ValidationError(
                {
                    'key_id': [
                        'Key "{}" not found.'.format(key_id)
                    ]
                }, code='invalid'
            )

        return DetachedSignature.objects.sign_document_version(
            document_version=self.context['document_version'], key=key,
            passphrase=passphrase, user=self.context['request'].user
        )


class SignEmbeddedSerializer(SignDetachedSerializer):
    class Meta:
        fields = (
            'date', 'document_version_url', 'key_id', 'signature_id',
            'passphrase', 'public_key_fingerprint', 'url'
        )
        model = EmbeddedSignature

    def sign(self, key_id, passphrase):
        key_queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_key_sign, queryset=Key.objects.all(),
            user=self.context['request'].user
        )

        try:
            key = key_queryset.get(fingerprint__endswith=key_id)
        except Key.DoesNotExist:
            raise ValidationError(
                {
                    'key_id': [
                        'Key "{}" not found.'.format(key_id)
                    ]
                }, code='invalid'
            )

        return EmbeddedSignature.objects.sign_document_version(
            document_version=self.context['document_version'], key=key,
            passphrase=passphrase, user=self.context['request'].user
        )
