from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template import TemplateSyntaxError
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.models import Document
from mayan.apps.views.generics import FormView
from mayan.apps.views.http import URL
from mayan.apps.views.mixins import ExternalObjectMixin

from .classes import Template
from .forms import DocumentTemplateSandboxForm
from .permissions import permission_template_sandbox


class DocumentTemplateSandboxView(ExternalObjectMixin, FormView):
    external_object_class = Document
    external_object_permission = permission_template_sandbox
    external_object_pk_url_kwarg = 'document_id'
    form_class = DocumentTemplateSandboxForm

    def form_valid(self, form):
        path = reverse(
            viewname='templating:document_template_sandbox',
            kwargs={'document_id': self.external_object.pk}
        )
        url = URL(
            path=path, query={'template': form.cleaned_data['template']}
        )

        return HttpResponseRedirect(redirect_to=url.to_string())

    def get_extra_context(self):
        return {
            'object': self.external_object,
            'title': _('Template sandbox for: %s') % self.external_object
        }

    def get_form_extra_kwargs(self):
        return {'model': Document, 'model_variable': 'document'}

    def get_initial(self):
        if settings.DEBUG:
            exception_list = (TemplateSyntaxError,)
        else:
            exception_list = (Exception, TemplateSyntaxError,)

        template_string = self.request.GET.get('template', '')
        try:
            template = Template(template_string=template_string)
            result = template.render(
                context={'document': self.external_object}
            )
        except exception_list as exception:
            result = ''
            error_message = _(
                'Template error; %(exception)s'
            ) % {
                'exception': exception
            }
            messages.error(request=self.request, message=error_message)

        return {
            'template': template_string, 'result': result
        }
