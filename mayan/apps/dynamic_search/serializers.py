from __future__ import absolute_import

from rest_framework import serializers

from .models import RecentSearch


class RecentSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecentSearch
        read_only_fields = ('user', 'query', 'datetime_created', 'hits')


class SearchSerializer(serializers.Serializer):
    results = serializers.CharField()
