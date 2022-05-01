from mayan.apps.common.serializers import ContentTypeSerializer
from mayan.apps.rest_api import serializers
from mayan.apps.rest_api.relations import MultiKwargHyperlinkedIdentityField

from .models import ErrorLogPartitionEntry


class ErrorLogPartitionEntrySerializer(serializers.ModelSerializer):
    content_type = ContentTypeSerializer(
        read_only=True, source='error_log_partition.content_type'
    )
    object_id = serializers.IntegerField(
        source='error_log_partition.object_id'
    )
    url = MultiKwargHyperlinkedIdentityField(
        view_name='rest_api:errorlogpartitionentry-detail',
        view_kwargs=(
            {
                'lookup_field': 'error_log_partition.content_type.app_label',
                'lookup_url_kwarg': 'app_label',
            },
            {
                'lookup_field': 'error_log_partition.content_type.model',
                'lookup_url_kwarg': 'model_name',
            },
            {
                'lookup_field': 'error_log_partition.object_id',
                'lookup_url_kwarg': 'object_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'error_log_partition_entry_id',
            }
        ),
    )

    class Meta:
        fields = (
            'content_type', 'datetime', 'id', 'object_id', 'text', 'url'
        )
        model = ErrorLogPartitionEntry
        read_only_fields = fields
