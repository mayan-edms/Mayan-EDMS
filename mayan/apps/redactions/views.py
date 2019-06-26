from __future__ import absolute_import, unicode_literals

import logging

from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.generics import (
    SingleObjectCreateView, SingleObjectDeleteView, SingleObjectEditView,
    SingleObjectListView
)
from mayan.apps.common.mixins import ExternalObjectMixin
from mayan.apps.converter.transformations import TransformationDrawRectanglePercent
from mayan.apps.documents.models import DocumentPage

from .forms import RedactionCoordinatesForm
from .icons import icon_redactions
from .links import link_redaction_create
from .models import Redaction
from .permissions import (
    permission_redaction_create, permission_redaction_delete,
    permission_redaction_edit, permission_redaction_view
)

logger = logging.getLogger(__name__)


class RedactionCreateView(ExternalObjectMixin, SingleObjectCreateView):
    external_object_class = DocumentPage
    external_object_pk_url_kwarg = 'pk'
    form_class = RedactionCoordinatesForm
    model = Redaction
    object_permission = permission_redaction_create
    template_name = 'redactions/cropper.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.content_object = self.external_object
        instance.name = TransformationDrawRectanglePercent.name
        instance.save()
        return super(RedactionCreateView, self).form_valid(form)

    def get_extra_context(self, **kwargs):
        context = {
            'document_page': self.external_object,
            'redaction': self.object,
            'title': _('Create redaction for: %s') % self.external_object
        }

        return context

    def get_post_action_redirect(self):
        return reverse(
            viewname='redactions:redaction_list', kwargs={
                'pk': self.external_object.pk
            }
        )


class RedactionDeleteView(SingleObjectDeleteView):
    model = Redaction
    object_permission = permission_redaction_delete

    def get_post_action_redirect(self):
        return reverse(
            viewname='redactions:redaction_list', kwargs={
                'pk': self.object.content_object.pk
            }
        )

    def get_extra_context(self):
        return {
            'content_object': self.object.content_object,
            'navigation_object_list': ('content_object', 'redaction'),
            'previous': reverse(
                viewname='redactions:redaction_list', kwargs={
                    'pk': self.object.content_object.pk
                }
            ),
            'redaction': self.object,
            'title': _(
                'Delete refaction for: %(content_object)s?'
            ) % {
                'content_object': self.object.content_object
            },
        }


class RedactionEditView(SingleObjectEditView):
    form_class = RedactionCoordinatesForm
    model = Redaction
    object_permission = permission_redaction_edit
    template_name = 'redactions/cropper.html'

    def get_extra_context(self, **kwargs):
        context = {
            'document_page': self.object.content_object,
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
    object_permission = permission_redaction_view
    external_object_pk_url_kwarg = 'pk'

    def dispatch(self, request, *args, **kwargs):
        return super(RedactionListView, self).dispatch(
            request, *args, **kwargs
        )

    def get_extra_context(self):
        return {
            'hide_object': True,
            'object': self.external_object,
            'no_results_icon': icon_redactions,
            'no_results_main_link': link_redaction_create.resolve(
                context=RequestContext(
                    request=self.request, dict_={
                        'object': self.external_object
                    }
                )
            ),
            'no_results_text': _(
                'Redactions allow removing access to confidential and '
                'sensitive information without having to modify the document.'
            ),
            'no_results_title': _('No existing redactions'),
            'title': _('Redactions for: %s') % self.external_object,
        }

    def get_source_queryset(self):
        return Redaction.objects.get_for_object(
            obj=self.external_object
        ).filter(name__startswith='draw')
