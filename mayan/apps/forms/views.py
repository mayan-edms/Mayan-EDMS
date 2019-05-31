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

"""
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
"""


from .forms import FormInstanceDynamicForm

class FormInstanceCreateView(ExternalObjectMixin, SingleObjectDynamicFormCreateView):
    external_object_class = FormTemplate
    external_object_pk_url_kwarg = 'pk'
    form_class = FormInstanceDynamicForm
    #post_action_redirect = reverse_lazy(viewname='mailer:user_mailer_list')
    #view_permission = permission_user_mailer_create

    #def get_backend(self):
    #    try:
    #        return MailerBackend.get(name=self.kwargs['class_path'])
    #    except KeyError:
    #        raise Http404(
    #            '{} class not found'.format(self.kwargs['class_path'])
    #        )

    #def get_extra_context(self):
    #    return {
    #        'title': _(
    #            'Create a "%s" mailing profile'
    #        ) % self.get_backend().label,
    #    }

    def get_form_schema(self):
        result = {
            'fields': self.external_object.get_fields_dictionary(),
            'widgets': {}
        }

        return result


    #def get_form_schema(self):
    #    backend = self.get_backend()
    #    result = {
    #        'fields': backend.fields,
    #        'widgets': getattr(backend, 'widgets', {})
    #    }
    #    if hasattr(backend, 'field_order'):
    #        result['field_order'] = backend.field_order

    #    return result

    def get_instance_extra_data(self):
        return {'form_template': self.external_object}


class FormInstanceEditView(SingleObjectDynamicFormEditView):
    model = FormInstance
    form_class = FormInstanceDynamicForm

    def get_form_schema(self):
        result = {
            'fields': self.object.form_template.get_fields_dictionary(),
            'widgets': {}
        }

        return result
