from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

from mayan.apps.common.generics import (
    MultipleObjectConfirmActionView, SingleObjectListView
)

from .models import Cache
from .permissions import permission_cache_purge, permission_cache_view

from .tasks import task_cache_purge


class CacheListView(SingleObjectListView):
    model = Cache
    object_permission = permission_cache_view

    def get_extra_context(self):
        return {
            'hide_object': True,
            'title': _('File caches list')
        }


class CachePurgeView(MultipleObjectConfirmActionView):
    model = Cache
    object_permission = permission_cache_purge
    pk_url_kwarg = 'cache_id'
    success_message_singular = '%(count)d cache submitted for purging.'
    success_message_plural = '%(count)d caches submitted for purging.'

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'title': ungettext(
                singular='Submit the selected cache for purging?',
                plural='Submit the selected caches for purging?',
                number=queryset.count()
            )
        }

        if queryset.count() == 1:
            result['object'] = queryset.first()

        return result

    def object_action(self, form, instance):
        task_cache_purge.apply_async(
            kwargs={'cache_id': instance.pk, 'user_id': self.request.user.pk}
        )
