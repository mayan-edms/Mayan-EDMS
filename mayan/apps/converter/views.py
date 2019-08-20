from __future__ import absolute_import, unicode_literals

import logging

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.generics import (
    FormView, SingleObjectCreateView, SingleObjectDeleteView,
    SingleObjectEditView, SingleObjectListView
)
from mayan.apps.common.mixins import ExternalContentTypeObjectMixin

from .classes import Layer
from .forms import LayerTransformationForm, LayerTransformationSelectForm
from .links import link_transformation_select
from .models import LayerTransformation, ObjectLayer
from .transformations import BaseTransformation

logger = logging.getLogger(__name__)


class LayerViewMixin(object):
    def dispatch(self, request, *args, **kwargs):
        self.layer = self.get_layer()
        return super(LayerViewMixin, self).dispatch(
            request=request, *args, **kwargs
        )

    def get_layer(self):
        return Layer.get(
            name=self.kwargs['layer_name']
        )


class TransformationCreateView(
    LayerViewMixin, ExternalContentTypeObjectMixin, SingleObjectCreateView
):
    form_class = LayerTransformationForm

    def form_valid(self, form):
        layer = self.layer
        content_type = self.get_content_type()
        object_layer, created = ObjectLayer.objects.get_or_create(
            content_type=content_type, object_id=self.external_object.pk,
            stored_layer=layer.stored_layer
        )

        instance = form.save(commit=False)
        instance.content_object = self.external_object
        instance.name = self.kwargs['transformation_name']
        instance.object_layer = object_layer
        try:
            instance.full_clean()
            instance.save()
        except Exception as exception:
            logger.debug('Invalid form, exception: %s', exception)
            return super(TransformationCreateView, self).form_invalid(form)
        else:
            return super(TransformationCreateView, self).form_valid(form)

    def get_extra_context(self):
        return {
            'content_object': self.external_object,
            'form_field_css_classes': 'hidden' if hasattr(
                self.get_transformation_class(), 'template_name'
            ) else '',
            'layer': self.layer,
            'layer_name': self.layer.name,
            'navigation_object_list': ('content_object',),
            'title': _(
                'Create layer "%(layer)s" transformation '
                '"%(transformation)s" for: %(object)s'
            ) % {
                'layer': self.layer,
                'transformation': self.get_transformation_class(),
                'object': self.external_object,
            }
        }

    def get_form_extra_kwargs(self):
        return {
            'transformation_name': self.kwargs['transformation_name']
        }

    def get_external_object_permission(self):
        return self.layer.permissions.get('create', None)

    def get_post_action_redirect(self):
        return reverse(
            viewname='converter:transformation_list', kwargs={
                'app_label': self.kwargs['app_label'],
                'model': self.kwargs['model'],
                'object_id': self.kwargs['object_id'],
                'layer_name': self.kwargs['layer_name']
            }
        )

    def get_queryset(self):
        return self.layer.get_transformations_for(
            obj=self.content_object
        )

    def get_template_names(self):
        return [
            getattr(
                self.get_transformation_class(), 'template_name',
                self.template_name
            )
        ]

    def get_transformation_class(self):
        return BaseTransformation.get(name=self.kwargs['transformation_name'])


class TransformationDeleteView(LayerViewMixin, SingleObjectDeleteView):
    model = LayerTransformation

    def get_extra_context(self):
        return {
            'content_object': self.object.object_layer.content_object,
            'layer_name': self.layer.name,
            'navigation_object_list': ('content_object', 'transformation'),
            'previous': reverse(
                viewname='converter:transformation_list', kwargs={
                    'app_label': self.object.object_layer.content_type.app_label,
                    'model': self.object.object_layer.content_type.model,
                    'object_id': self.object.object_layer.object_id,
                    'layer_name': self.object.object_layer.stored_layer.name
                }
            ),
            'title': _(
                'Delete transformation "%(transformation)s" for: '
                '%(content_object)s?'
            ) % {
                'transformation': self.object,
                'content_object': self.object.object_layer.content_object
            },
            'transformation': self.object,
        }

    def get_object_permission(self):
        return self.layer.permissions.get('delete', None)

    def get_post_action_redirect(self):
        return reverse(
            viewname='converter:transformation_list', kwargs={
                'app_label': self.object.object_layer.content_type.app_label,
                'model': self.object.object_layer.content_type.model,
                'object_id': self.object.object_layer.object_id,
                'layer_name': self.object.object_layer.stored_layer.name
            }
        )


class TransformationEditView(LayerViewMixin, SingleObjectEditView):
    form_class = LayerTransformationForm
    model = LayerTransformation

    def form_valid(self, form):
        instance = form.save(commit=False)
        try:
            instance.full_clean()
            instance.save()
        except Exception as exception:
            logger.debug('Invalid form, exception: %s', exception)
            return super(TransformationEditView, self).form_invalid(form=form)
        else:
            return super(TransformationEditView, self).form_valid(form=form)

    def get_extra_context(self):
        return {
            'content_object': self.object.object_layer.content_object,
            'form_field_css_classes': 'hidden' if hasattr(
                self.object.get_transformation_class(), 'template_name'
            ) else '',
            'layer': self.layer,
            'layer_name': self.layer.name,
            'navigation_object_list': ('content_object', 'transformation'),
            'title': _(
                'Edit transformation "%(transformation)s" '
                'for: %(content_object)s'
            ) % {
                'transformation': self.object,
                'content_object': self.object.object_layer.content_object
            },
            'transformation': self.object,
        }

    def get_object_permission(self):
        return self.layer.permissions.get('edit', None)

    def get_post_action_redirect(self):
        return reverse(
            viewname='converter:transformation_list', kwargs={
                'app_label': self.object.object_layer.content_type.app_label,
                'model': self.object.object_layer.content_type.model,
                'object_id': self.object.object_layer.object_id,
                'layer_name': self.object.object_layer.stored_layer.name
            }
        )

    def get_template_names(self):
        return [
            getattr(
                self.object.get_transformation_class(), 'template_name',
                self.template_name
            )
        ]


class TransformationListView(
    LayerViewMixin, ExternalContentTypeObjectMixin, SingleObjectListView
):
    def get_external_object_permission(self):
        return self.layer.permissions.get('view', None)

    def get_extra_context(self):
        return {
            'object': self.external_object,
            'hide_link': True,
            'hide_object': True,
            'layer_name': self.layer.name,
            'no_results_icon': self.layer.get_icon(),
            'no_results_main_link': link_transformation_select.resolve(
                context=RequestContext(
                    request=self.request, dict_={
                        'resolved_object': self.external_object,
                        'layer_name': self.kwargs['layer_name'],
                    }
                )
            ),
            'no_results_text': self.layer.get_empty_results_text(),
            'no_results_title': _(
                'There are no entries for layer "%(layer_name)s"'
            ) % {'layer_name': self.layer.label},
            'title': _(
                'Layer "%(layer)s" transformations for: %(object)s'
            ) % {
                'layer': self.layer,
                'object': self.external_object,
            }
        }

    def get_source_queryset(self):
        return self.layer.get_transformations_for(obj=self.external_object)


class TransformationSelectView(
    ExternalContentTypeObjectMixin, LayerViewMixin, FormView
):
    form_class = LayerTransformationSelectForm
    template_name = 'appearance/generic_form.html'

    def form_valid(self, form):
        return HttpResponseRedirect(
            redirect_to=reverse(
                viewname='converter:transformation_create',
                kwargs={
                    'app_label': self.kwargs['app_label'],
                    'model': self.kwargs['model'],
                    'object_id': self.kwargs['object_id'],
                    'layer_name': self.kwargs['layer_name'],
                    'transformation_name': form.cleaned_data[
                        'transformation'
                    ]
                }
            )
        )

    def get_extra_context(self):
        return {
            'layer': self.layer,
            'layer_name': self.kwargs['layer_name'],
            'navigation_object_list': ('content_object',),
            'content_object': self.external_object,
            'submit_label': _('Select'),
            'title': _(
                'Select new layer "%(layer)s" transformation '
                'for: %(object)s'
            ) % {
                'layer': self.layer,
                'object': self.external_object,
            }
        }

    def get_form_extra_kwargs(self):
        return {
            'layer': self.layer
        }
