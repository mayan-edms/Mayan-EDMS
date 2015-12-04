from __future__ import unicode_literals

from rest_framework import serializers

from user_management.serializers import UserSerializer

from .models import RecentSearch


class RecentSearchSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='rest_api:recentsearch-detail'
    )
    user = UserSerializer()

    class Meta:
        fields = ('datetime_created', 'hits', 'query', 'url', 'user')
        model = RecentSearch
        read_only_fields = ('datetime_created', 'hits', 'query', 'user')
