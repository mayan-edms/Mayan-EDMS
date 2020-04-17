from rest_framework import serializers
from rest_framework.reverse import reverse


class EndpointSerializer(serializers.Serializer):
    label = serializers.CharField(read_only=True)

    url = serializers.SerializerMethodField()

    def get_url(self, instance):
        if instance.viewname:
            return reverse(
                viewname=instance.viewname, request=self.context['request'],
                format=self.context['format']
            )
