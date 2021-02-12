from rest_framework import serializers

from .models import Asset


class AssetSerializer(serializers.HyperlinkedModelSerializer):
    image_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='asset_id',
        view_name='rest_api:asset-image'
    )

    class Meta:
        extra_kwargs = {
            'url': {
                'lookup_url_kwarg': 'asset_id',
                'view_name': 'rest_api:asset-detail'
            },
        }
        fields = (
            'file', 'label', 'id', 'image_url', 'internal_name', 'url'
        )
        model = Asset
