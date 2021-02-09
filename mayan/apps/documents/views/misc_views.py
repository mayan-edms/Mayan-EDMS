from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.generics import FormView, SimpleView
from mayan.apps.views.mixins import ExternalObjectViewMixin

from ..forms.misc_forms import PrintForm
from ..literals import PAGE_RANGE_RANGE
from ..settings import setting_print_width, setting_print_height
from ..utils import parse_range


class PrintFormView(ExternalObjectViewMixin, FormView):
    external_object_class = None
    external_object_permission = None
    external_object_pk_url_kwarg = None
    form_class = PrintForm
    print_view_name = None
    print_view_kwarg = None

    def _add_recent_document(self):
        self.external_object.add_as_recent_document_for_user(
            user=self.request.user
        )

    def dispatch(self, request, *args, **kwargs):
        result = super().dispatch(request, *args, **kwargs)

        self._add_recent_document()

        return result

    def get_extra_context(self):
        return {
            'form_action': reverse(
                viewname=self.print_view_name, kwargs={
                    self.print_view_kwarg: self.external_object.pk
                }
            ),
            'object': self.external_object,
            'submit_label': _('Submit'),
            'submit_method': 'GET',
            'submit_target': '_blank',
            'title': _('Print: %s') % self.external_object,
        }


class DocumentPrintView(ExternalObjectViewMixin, SimpleView):
    external_object_class = None
    external_object_permission = None
    external_object_pk_url_kwarg = None
    template_name = 'documents/document_print.html'

    def _add_recent_document(self):
        self.external_object.add_as_recent_document_for_user(
            user=self.request.user
        )

    def dispatch(self, request, *args, **kwargs):
        result = super().dispatch(request, *args, **kwargs)

        self._add_recent_document()

        return result

    def get_extra_context(self):
        page_group = self.request.GET.get('page_group', None)
        page_range = self.request.GET.get('page_range', None)

        if page_group == PAGE_RANGE_RANGE:
            if page_range:
                page_range = parse_range(astr=page_range)
                pages = self.external_object.pages.filter(
                    page_number__in=page_range
                )
            else:
                pages = self.external_object.pages.all()
        else:
            pages = self.external_object.pages.all()

        return {
            'appearance_type': 'plain',
            'pages': pages,
            'width': setting_print_width.value,
            'height': setting_print_height.value,
        }
