from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Source


class SourceSerializer(serializers.HyperlinkedModelSerializer):
    actions = serializers.SerializerMethodField()

    class Meta:
        extra_kwargs = {
            'url': {
                'lookup_field': 'pk', 'lookup_url_kwarg': 'source_id',
                'view_name': 'rest_api:source-detail'
            },
        }
        fields = (
            'actions', 'backend_data', 'backend_path', 'enabled', 'id',
            'label', 'url'
        )
        model = Source
        read_only_fields = ('actions', 'id', 'url')

    def get_actions(self, instance):
        result = []

        for action in instance.get_actions():
            result.append(
                {
                    'name': action.name,
                    'arguments': action.arguments,
                    'url': reverse(
                        viewname='rest_api:source-action', kwargs={
                            'source_id': instance.pk,
                            'action_name': action.name
                        }, request=self.context['request'],
                        format=self.context['format']
                    )
                }
            )

        return result


class SourceBackendActionSerializer(serializers.Serializer):
    arguments = serializers.JSONField(
        help_text=_(
            'Optional arguments for the action. Must be JSON formatted.'
        ), label=_('Arguments'), required=False
    )
