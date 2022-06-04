import logging

from django.contrib import messages
from django.template import RequestContext
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _, ungettext

from mayan.apps.views.generics import (
    MultipleObjectConfirmActionView, SingleObjectCreateView,
    SingleObjectDetailView, SingleObjectEditView, SingleObjectListView
)

from ..forms import AssetDetailForm
from ..icons import (
    icon_asset_create, icon_asset_delete, icon_asset_detail, icon_asset_edit,
    icon_asset_list
)
from ..links import link_asset_create
from ..models import Asset
from ..permissions import (
    permission_asset_create, permission_asset_delete,
    permission_asset_edit, permission_asset_view
)

logger = logging.getLogger(name=__name__)


class AssetCreateView(SingleObjectCreateView):
    fields = ('label', 'internal_name', 'file')
    model = Asset
    view_icon = icon_asset_create
    view_permission = permission_asset_create

    def get_extra_context(self):
        return {
            'title': _('Create asset'),
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class AssetDeleteView(MultipleObjectConfirmActionView):
    model = Asset
    object_permission = permission_asset_delete
    pk_url_kwarg = 'asset_id'
    post_action_redirect = reverse_lazy(viewname='converter:asset_list')
    success_asset = _('Delete request performed on %(count)d asset')
    success_asset_plural = _(
        'Delete request performed on %(count)d assets'
    )
    view_icon = icon_asset_delete

    def get_extra_context(self):
        result = {
            'delete_view': True,
            'title': ungettext(
                singular='Delete the selected asset?',
                plural='Delete the selected assets?',
                number=self.object_list.count()
            )
        }

        if self.object_list.count() == 1:
            result.update(
                {
                    'object': self.object_list.first(),
                    'title': _('Delete asset: %s?') % self.object_list.first()
                }
            )

        return result

    def object_action(self, instance, form=None):
        try:
            instance.delete()
            messages.success(
                message=_(
                    'Asset "%s" deleted successfully.'
                ) % instance, request=self.request
            )
        except Exception as exception:
            messages.error(
                message=_('Error deleting asset "%(asset)s": %(error)s') % {
                    'asset': instance, 'error': exception
                }, request=self.request
            )


class AssetDetailView(SingleObjectDetailView):
    form_class = AssetDetailForm
    model = Asset
    object_permission = permission_asset_view
    pk_url_kwarg = 'asset_id'
    view_icon = icon_asset_detail

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _('Details asset: %s') % self.object,
        }


class AssetEditView(SingleObjectEditView):
    fields = ('label', 'internal_name', 'file')
    model = Asset
    object_permission = permission_asset_edit
    pk_url_kwarg = 'asset_id'
    post_action_redirect = reverse_lazy(viewname='converter:asset_list')
    view_icon = icon_asset_edit

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _('Edit asset: %s') % self.object,
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class AssetListView(SingleObjectListView):
    model = Asset
    object_permission = permission_asset_view
    view_icon = icon_asset_list

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_asset_list,
            'no_results_main_link': link_asset_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Assets are files that can be used in conjuction with '
                'certain transformations.'
            ),
            'no_results_title': _('No assets available'),
            'title': _('Assets'),
        }
