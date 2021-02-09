from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.generics import ConfirmView, SingleObjectListView
from mayan.apps.views.mixins import ExternalContentTypeObjectViewMixin

from .icons import icon_object_errors
from .permissions import permission_error_log_view


class ObjectErrorLogEntryListClearView(
    ExternalContentTypeObjectViewMixin, ConfirmView
):
    external_object_permission = permission_error_log_view

    def get_extra_context(self):
        return {
            'object': self.external_object,
            'title': _(
                'Clear error log entries for: %s' % self.external_object
            ),
        }

    def view_action(self):
        self.external_object.error_log.all().delete()
        messages.success(
            message=_('Object error log cleared successfully'),
            request=self.request
        )


class ObjectErrorLogEntryListView(
    ExternalContentTypeObjectViewMixin, SingleObjectListView
):
    external_object_permission = permission_error_log_view

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_object_errors,
            'no_results_text': _(
                'This view displays the error log of different object. '
                'An empty list is a good thing.'
            ),
            'no_results_title': _(
                'There are no error log entries'
            ),
            'object': self.external_object,
            'title': _('Error log entries for: %s' % self.external_object),
        }

    def get_source_queryset(self):
        return self.external_object.error_log.all()
