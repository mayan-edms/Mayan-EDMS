from rest_framework import serializers
from rest_framework.reverse import reverse


class BlankSerializer(serializers.Serializer):
    """Serializer for the object action API view"""


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
