import logging

from django.template import RequestContext
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.generics import (
    MultipleObjectConfirmActionView, SingleObjectCreateView,
    SingleObjectEditView, SingleObjectListView
)

from .icons import icon_announcement_list
from .links import link_announcement_create
from .models import Announcement
from .permissions import (
    permission_announcement_create, permission_announcement_delete,
    permission_announcement_edit, permission_announcement_view
)

logger = logging.getLogger(name=__name__)


class AnnouncementCreateView(SingleObjectCreateView):
    fields = ('label', 'text', 'enabled', 'start_datetime', 'end_datetime')
    model = Announcement
    view_permission = permission_announcement_create

    def get_extra_context(self):
        return {
            'title': _('Create announcement'),
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class AnnouncementDeleteView(MultipleObjectConfirmActionView):
    error_message = _(
        'Error deleting announcement "%(instance)s"; %(exception)s'
    )
    model = Announcement
    object_permission = permission_announcement_delete
    pk_url_kwarg = 'announcement_id'
    post_action_redirect = reverse_lazy(
        viewname='announcements:announcement_list'
    )
    success_message_single = _(
        'Announcement "%(object)s" deleted successfully.'
    )
    success_message_singular = _(
        '%(count)d announcement deleted successfully.'
    )
    success_message_plural = _(
        '%(count)d announcements deleted successfully.'
    )
    title_single = _('Delete announcement: %(object)s.')
    title_singular = _('Delete the %(count)d selected announcement.')
    title_plural = _('Delete the %(count)d selected announcements.')

    def get_extra_context(self):
        context = {
            'delete_view': True,
        }

        if self.object_list.count() == 1:
            context.update(
                {
                    'object': self.object_list.first(),
                }
            )

        return context

    def object_action(self, instance, form=None):
        instance.delete()


class AnnouncementEditView(SingleObjectEditView):
    fields = ('label', 'text', 'enabled', 'start_datetime', 'end_datetime')
    model = Announcement
    object_permission = permission_announcement_edit
    pk_url_kwarg = 'announcement_id'
    post_action_redirect = reverse_lazy(
        viewname='announcements:announcement_list'
    )

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _('Edit announcement: %s') % self.object,
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class AnnouncementListView(SingleObjectListView):
    model = Announcement
    object_permission = permission_announcement_view

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_announcement_list,
            'no_results_main_link': link_announcement_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Announcements are displayed in the login view. You can use '
                'announcements to convery information about your organzation, '
                'announcements or usage guidelines for your users.'
            ),
            'no_results_title': _('No announcements available'),
            'title': _('Announcements'),
        }
