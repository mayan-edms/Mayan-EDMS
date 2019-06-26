from __future__ import absolute_import, unicode_literals

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.generics import (
    SingleObjectCreateView, SingleObjectEditView, SingleObjectListView
)
from mayan.apps.common.mixins import ExternalObjectMixin
from mayan.apps.converter.models import Transformation
from mayan.apps.converter.transformations import TransformationDrawRectangle
from mayan.apps.converter.views import TransformationListView
from mayan.apps.documents.models import Document, DocumentPage

from .forms import RedactionCoordinatesForm, RedactionForm
from .icons import icon_redactions
from .models import Redaction


class RedactionCreateView(ExternalObjectMixin, SingleObjectCreateView):
    external_object_class = DocumentPage
    external_object_pk_url_kwarg = 'pk'
    form_class = RedactionForm
    model = Redaction
    #object_permission =

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.name = TransformationDrawRectangle.name
        instance.content_object = self.external_object
        instance.save()

        #messages.success(self.request, _('Redaction created successfully.'))

        return HttpResponseRedirect(self.get_success_url())

    def get_extra_context(self, **kwargs):
        return {
            'object': self.external_object,
            'title': _(
                'Create redaction for document page: %s'
            ) % self.external_object
        }

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(RedactionCreateView, self).get_form_kwargs()
        kwargs.update({'document_page': self.external_object})
        return kwargs

    def get_post_action_redirect(self):
        return reverse(
            viewname='redactions:redaction_list', kwargs={
                'pk': self.external_object.pk
            }
        )


class RedactionEditView(SingleObjectEditView):
    form_class = RedactionCoordinatesForm
    model = Redaction
    #object_permission =
    #page_kwarg = 'page'
    #paginate_by = 1
    template_name = 'redactions/cropper.html'

    def get_extra_context(self, **kwargs):
        context = {
            #'api_image_data_url': document.get_api_image_url,
            'document_page': self.object.content_object,
            'hide_help_text': True,
            'hide_required_text': True,
            'hide_title': True,
            'navigation_object_list': ['document_page', 'redaction'],
            'redaction': self.object,
            'title': _('Edit redaction: %s') % self.object
        }


        return context

    def get_post_action_redirect(self):
        return reverse(
            viewname='redactions:redaction_list', kwargs={
                'pk': self.object.content_object.pk
            }
        )


class RedactionListView(ExternalObjectMixin, SingleObjectListView):
    external_object_class = DocumentPage
    #external_object_permission =
    external_object_pk_url_kwarg = 'pk'

    def dispatch(self, request, *args, **kwargs):
        return super(RedactionListView, self).dispatch(
            request, *args, **kwargs
        )

    def get_extra_context(self):
        return {
            'object': self.external_object,
            #'hide_link': True,
            #'hide_object': True,
            #'navigation_object_list': ('content_object',),
            'no_results_icon': icon_redactions,
            #'no_results_main_link': link_transformation_create.resolve(
            #    context=RequestContext(
            #        request=self.request, dict_={
            #            'content_object': self.content_object
            #        }
            #    )
            #),
            #'no_results_text': _(
            #    'Transformations allow changing the visual appearance '
            #    'of documents without making permanent changes to the '
            #    'document file themselves.'
            #),
            'no_results_title': _('No redactions exist'),
            'title': _('Redactions for: %s') % self.external_object,
        }

    def get_source_queryset(self):
        return Transformation.objects.get_for_object(
            obj=self.external_object
        ).filter(name__startswith='draw')

        result = Transformation.objects.none()

        for version in self.external_object.versions.all():
            for page in version.pages.all():
                result = result | Transformation.objects.get_for_object(obj=page)

        return result.filter(name__startswith='draw')
        #return Transformation.objects.get_for_object(obj=self.external_object)

