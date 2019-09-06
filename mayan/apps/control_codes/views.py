from __future__ import absolute_import, unicode_literals

import logging

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.generics import (
    FormView, SingleObjectCreateView, SingleObjectDeleteView,
    SingleObjectDetailView, SingleObjectEditView, SingleObjectListView
)
from mayan.apps.common.mixins import ExternalObjectMixin

from .classes import ControlCode
from .forms import ControlSheetCodeClassSelectionForm, ControlSheetCodeForm
from .icons import icon_control_sheet, icon_control_sheet_code
from .links import link_control_sheet_create, link_control_sheet_code_select
from .models import ControlSheet
from .permissions import (
    permission_control_sheet_create, permission_control_sheet_delete,
    permission_control_sheet_edit, permission_control_sheet_view
)

logger = logging.getLogger(__name__)


class ControlSheetCreateView(SingleObjectCreateView):
    fields = ('label',)
    model = ControlSheet
    view_permission = permission_control_sheet_create

    def get_extra_context(self):
        return {
            'title': _('Create new control sheet')
        }


class ControlSheetDeleteView(SingleObjectDeleteView):
    model = ControlSheet
    object_permission = permission_control_sheet_delete
    pk_url_kwarg = 'control_sheet_id'

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _(
                'Delete control sheet: %s?'
            ) % self.object
        }


class ControlSheetEditView(SingleObjectEditView):
    fields = ('label',)
    model = ControlSheet
    object_permission = permission_control_sheet_edit
    pk_url_kwarg = 'control_sheet_id'

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _(
                'Edit control sheet: %s'
            ) % self.object
        }


class ControlSheetListView(SingleObjectListView):
    model = ControlSheet
    object_permission = permission_control_sheet_view

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_control_sheet,
            'no_results_main_link': link_control_sheet_create.resolve(
                context=RequestContext(request=self.request,)
            ),
            'no_results_text': _(
                'Control sheets contain barcodes that are scanned together '
                'with the document to automate how that document will be '
                'processed.'
            ),
            'no_results_title': _('There are no control sheets'),
            'title': _('Control sheets')
        }


class ControlSheetPreviewView(SingleObjectDetailView):
    fields = ('label',)
    pk_url_kwarg = 'control_sheet_id'
    model = ControlSheet
    object_permission = permission_control_sheet_view
    template_name = 'control_codes/control_sheet_preview.html'

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _(
                'Preview of control sheet: %s'
            ) % self.object
        }


class ControlSheetPrintView(ControlSheetPreviewView):
    template_name = 'control_codes/control_sheet_print.html'

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _(
                'Control sheet: %s'
            ) % self.object
        }


class ControlSheetCodeCreate(ExternalObjectMixin, SingleObjectCreateView):
    external_object_class = ControlSheet
    external_object_permission = permission_control_sheet_edit
    external_object_pk_url_kwarg = 'control_sheet_id'
    form_class = ControlSheetCodeForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.control_sheet = self.external_object
        try:
            instance.name = self.get_control_code_class().name
            instance.full_clean()
            instance.save()
        except Exception as exception:
            logger.error('Invalid form, exception: %s', exception)
            return super(ControlSheetCodeCreate, self).form_invalid(form=form)
        else:
            return super(ControlSheetCodeCreate, self).form_valid(form=form)

    def get_control_code_class(self):
        return ControlCode.get(name=self.kwargs['control_code_class_name'])

    def get_extra_context(self):
        return {
            'control_sheet': self.external_object,
            'navigation_object_list': ('control_sheet',),
            'title': _(
                'Create code "%(control_code)s" for: %(control_sheet)s'
            ) % {
                'control_code': self.get_control_code_class().label,
                'control_sheet': self.external_object,
            }
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='control_codes:control_sheet_code_list', kwargs={
                'control_sheet_id': self.external_object.pk,
            }
        )

    def get_source_queryset(self):
        return self.external_object.codes.all()


class ControlSheetCodeDeleteView(ExternalObjectMixin, SingleObjectDeleteView):
    form_class = ControlSheetCodeForm
    external_object_class = ControlSheet
    external_object_permission = permission_control_sheet_edit
    external_object_pk_url_kwarg = 'control_sheet_id'
    pk_url_kwarg = 'control_sheet_code_id'

    def get_extra_context(self):
        return {
            'control_sheet': self.external_object,
            'hide_object': True,
            'navigation_object_list': ('control_sheet', 'object',),
            'object': self.object,
            'title': _('Delete control sheet code: %s') % self.object,
        }

    def get_source_queryset(self):
        return self.external_object.codes.all()


class ControlSheetCodeEditView(ExternalObjectMixin, SingleObjectEditView):
    form_class = ControlSheetCodeForm
    external_object_class = ControlSheet
    external_object_permission = permission_control_sheet_edit
    external_object_pk_url_kwarg = 'control_sheet_id'
    pk_url_kwarg = 'control_sheet_code_id'

    def get_extra_context(self):
        return {
            'control_sheet': self.external_object,
            'hide_object': True,
            'navigation_object_list': ('control_sheet', 'object',),
            'object': self.object,
            'title': _('Edit control sheet code: %s') % self.object,
        }

    def get_source_queryset(self):
        return self.external_object.codes.all()


class ControlSheetCodeListView(ExternalObjectMixin, SingleObjectListView):
    external_object_class = ControlSheet
    external_object_permission = permission_control_sheet_view
    external_object_pk_url_kwarg = 'control_sheet_id'

    def get_extra_context(self):
        return {
            'control_sheet': self.external_object,
            'hide_object': True,
            'navigation_object_list': ('control_sheet',),
            'no_results_icon': icon_control_sheet_code,
            'no_results_main_link': link_control_sheet_code_select.resolve(
                context=RequestContext(
                    request=self.request, dict_={
                        'control_sheet': self.external_object,
                    }
                )
            ),
            'no_results_text': _(
                'Control sheet codes are barcodes that trigger a specific '
                'process when they are scanned.'
            ),
            'no_results_title': _('There are no control sheet codes'),
            'title': _('Codes of control sheet: %s') % self.external_object,
        }

    def get_source_queryset(self):
        return self.external_object.codes.all()


class ControlSheetCodeSelectView(ExternalObjectMixin, FormView):
    external_object_class = ControlSheet
    external_object_permission = permission_control_sheet_edit
    external_object_pk_url_kwarg = 'control_sheet_id'
    form_class = ControlSheetCodeClassSelectionForm
    template_name = 'appearance/generic_form.html'

    def form_valid(self, form):
        return HttpResponseRedirect(
            redirect_to=reverse(
                viewname='control_codes:control_sheet_code_create',
                kwargs={
                    'control_sheet_id': self.external_object.pk,
                    'control_code_class_name': form.cleaned_data[
                        'control_code_class_name'
                    ]
                }
            )
        )

    def get_extra_context(self):
        return {
            'control_sheet': self.external_object,
            'navigation_object_list': ('control_sheet',),
            'submit_label': _('Select'),
            'title': _(
                'Select new control sheet code '
                'for: %(control_sheet)s'
            ) % {
                'control_sheet': self.external_object,
            }
        }
