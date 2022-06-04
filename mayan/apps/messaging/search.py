from mayan.apps.dynamic_search.classes import SearchModel

from .permissions import permission_message_view


search_model_message = SearchModel(
    app_label='messaging', model_name='Message',
    permission=permission_message_view,
    serializer_path='mayan.apps.messaging.serializers.MessageSerializer'
)
search_model_message.add_model_field(field='date_time')
search_model_message.add_model_field(field='subject')
search_model_message.add_model_field(field='body')
