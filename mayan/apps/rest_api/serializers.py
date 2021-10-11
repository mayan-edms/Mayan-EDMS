from rest_framework import serializers
from rest_framework.reverse import reverse

from .classes import BatchRequestCollection


class BatchAPIRequestResponseSerializer(serializers.Serializer):
    data = serializers.JSONField(read_only=True)
    headers = serializers.DictField(read_only=True)
    name = serializers.CharField(read_only=True)
    status_code = serializers.IntegerField(read_only=True)
    requests = serializers.JSONField(
        style={'base_template': 'textarea.html'},
        write_only=True
    )

    def validate(self, data):
        try:
            BatchRequestCollection(request_list=data['requests'])
        except Exception as exception:
            raise serializers.ValidationError(
                'Error validating requests; {}'.format(exception)
            )

        return data


class BlankSerializer(serializers.Serializer):
    """Serializer for the object action API view."""


class EndpointSerializer(serializers.Serializer):
    label = serializers.CharField(read_only=True)
    url = serializers.SerializerMethodField()

    def get_url(self, instance):
        if instance.viewname:
            return reverse(
                kwargs=instance.kwargs, viewname=instance.viewname,
                request=self.context['request'],
                format=self.context['format']
            )


class ProjectInformationSerializer(serializers.Serializer):
    __title__ = serializers.CharField(read_only=True)
    __version__ = serializers.CharField(read_only=True)
    __build__ = serializers.CharField(read_only=True)
    __build_string__ = serializers.CharField(read_only=True)
    __django_version__ = serializers.CharField(read_only=True)
    __author__ = serializers.CharField(read_only=True)
    __author_email__ = serializers.CharField(read_only=True)
    __description__ = serializers.CharField(read_only=True)
    __license__ = serializers.CharField(read_only=True)
    __copyright__ = serializers.CharField(read_only=True)
    __website__ = serializers.CharField(read_only=True)
