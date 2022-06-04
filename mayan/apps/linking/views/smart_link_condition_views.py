import logging

from django.template import RequestContext
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.generics import (
    SingleObjectCreateView, SingleObjectDeleteView, SingleObjectEditView,
    SingleObjectListView
)
from mayan.apps.views.mixins import ExternalObjectViewMixin

from ..forms import SmartLinkConditionForm
from ..icons import (
    icon_smart_link_condition, icon_smart_link_condition_create,
    icon_smart_link_condition_delete, icon_smart_link_condition_edit,
    icon_smart_link_condition_list
)
from ..links import link_smart_link_condition_create
from ..models import SmartLink, SmartLinkCondition
from ..permissions import permission_smart_link_edit

logger = logging.getLogger(name=__name__)


class SmartLinkConditionListView(ExternalObjectViewMixin, SingleObjectListView):
    external_object_class = SmartLink
    external_object_permission = permission_smart_link_edit
    external_object_pk_url_kwarg = 'smart_link_id'
    view_icon = icon_smart_link_condition_list

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_smart_link_condition,
            'no_results_main_link': link_smart_link_condition_create.resolve(
                context=RequestContext(
                    request=self.request, dict_={
                        'object': self.external_object
                    }
                )
            ),
            'no_results_text': _(
                'Conditions are small logic units that when combined '
                'define how the smart link will behave.'
            ),
            'no_results_title': _(
                'There are no conditions for this smart link'
            ),
            'object': self.external_object,
            'title': _(
                'Conditions for smart link: %s'
            ) % self.external_object,
        }

    def get_source_queryset(self):
        return self.external_object.conditions.all()


class SmartLinkConditionCreateView(
    ExternalObjectViewMixin, SingleObjectCreateView
):
    external_object_class = SmartLink
    external_object_permission = permission_smart_link_edit
    external_object_pk_url_kwarg = 'smart_link_id'
    form_class = SmartLinkConditionForm
    view_icon = icon_smart_link_condition_create

    def get_extra_context(self):
        return {
            'title': _(
                'Add new conditions to smart link: "%s"'
            ) % self.external_object,
            'object': self.external_object,
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
            'smart_link': self.external_object
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='linking:smart_link_condition_list', kwargs={
                'smart_link_id': self.external_object.pk
            }
        )

    def get_queryset(self):
        return self.external_object.conditions.all()


class SmartLinkConditionDeleteView(SingleObjectDeleteView):
    model = SmartLinkCondition
    object_permission = permission_smart_link_edit
    pk_url_kwarg = 'smart_link_condition_id'
    view_icon = icon_smart_link_condition_delete

    def get_extra_context(self):
        return {
            'condition': self.object,
            'navigation_object_list': ('object', 'condition'),
            'object': self.object.smart_link,
            'title': _(
                'Delete smart link condition: "%s"?'
            ) % self.object,
        }

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}

    def get_post_action_redirect(self):
        return reverse(
            viewname='linking:smart_link_condition_list', kwargs={
                'smart_link_id': self.object.smart_link.pk
            }
        )


class SmartLinkConditionEditView(SingleObjectEditView):
    form_class = SmartLinkConditionForm
    model = SmartLinkCondition
    object_permission = permission_smart_link_edit
    pk_url_kwarg = 'smart_link_condition_id'
    view_icon = icon_smart_link_condition_edit

    def get_extra_context(self):
        return {
            'condition': self.object,
            'navigation_object_list': ('object', 'condition'),
            'object': self.object.smart_link,
            'title': _('Edit smart link condition'),
        }

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}

    def get_post_action_redirect(self):
        return reverse(
            viewname='linking:smart_link_condition_list', kwargs={
                'smart_link_id': self.object.smart_link.pk
            }
        )
