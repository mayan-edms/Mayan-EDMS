from __future__ import absolute_import, unicode_literals

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.utils.translation import ungettext, ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.common.generics import (
    DynamicFormView, FormView, MultipleObjectFormActionView, SingleObjectDeleteView,
    SingleObjectDynamicFormCreateView, SingleObjectDynamicFormEditView,
    SingleObjectListView
)
from mayan.apps.common.forms import DynamicForm, DynamicModelForm
from mayan.apps.common.mixins import ExternalObjectMixin

from .models import FormTemplate, FormInstance


class FormInstanceCreateView(ExternalObjectMixin, DynamicFormView):
    external_object_class = FormTemplate
    external_object_pk_url_kwarg = 'pk'
    form_class = DynamicForm

    def get_form_schema(self):
        result = {
            'fields': self.external_object.get_fields_dictionary(),
            'widgets': {}
        }

        return result
