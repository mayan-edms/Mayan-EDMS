from rest_framework import serializers

from mayan.apps.user_management.serializers import UserSerializer
from mayan.apps.rest_api.relations import MultiKwargHyperlinkedIdentityField

from .models import Comment


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'document_id',
                'lookup_url_kwarg': 'document_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'comment_id',
            },
        ),
        view_name='rest_api:comment-detail'
    )
    user = UserSerializer(read_only=True)

    class Meta:
        fields = ('id', 'submit_date', 'text', 'url', 'user')
        model = Comment
        read_only_field = ('id', 'submit_date', 'url', 'user')
