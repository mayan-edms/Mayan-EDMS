import logging

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _, ungettext

from mayan.apps.views.generics import (
    FormView, MultipleObjectConfirmActionView, SingleObjectCreateView,
    SingleObjectDeleteView, SingleObjectEditView, SingleObjectListView
)
from mayan.apps.views.mixins import ExternalContentTypeObjectMixin

from .forms import LayerTransformationForm, LayerTransformationSelectForm
from .icons import icon_asset_list
from .links import link_asset_create, link_transformation_select
from .models import Asset, LayerTransformation, ObjectLayer
from .permissions import (
    permission_asset_create, permission_asset_delete,
    permission_asset_edit, permission_asset_view
)
from .transformations import BaseTransformation
from .view_mixins import LayerViewMixin

logger = logging.getLogger(name=__name__)


class AssetCreateView(SingleObjectCreateView):
    fields = ('label', 'internal_name', 'file')
    model = Asset
    view_permission = permission_asset_create

    def get_extra_context(self):
        return {
            'title': _('Create asset'),
        }


class AssetDeleteView(MultipleObjectConfirmActionView):
    model = Asset
    object_permission = permission_asset_delete
    pk_url_kwarg = 'asset_id'
    post_action_redirect = reverse_lazy(viewname='converter:asset_list')
    success_asset = _('Delete request performed on %(count)d asset')
    success_asset_plural = _(
        'Delete request performed on %(count)d assets'
    )

    def get_extra_context(self):
        result = {
            'delete_view': True,
            'title': ungettext(
                singular='Delete the selected asset?',
                plural='Delete the selected assets?',
                number=self.object_list.count()
            )
        }

        if self.object_list.count() == 1:
            result.update(
                {
                    'object': self.object_list.first(),
                    'title': _('Delete asset: %s?') % self.object_list.first()
                }
            )

        return result

    def object_action(self, instance, form=None):
        try:
            instance.delete()
            messages.success(
                message=_(
                    'Asset "%s" deleted successfully.'
                ) % instance, request=self.request
            )
        except Exception as exception:
            messages.error(
                message=_('Error deleting asset "%(asset)s": %(error)s') % {
                    'asset': instance, 'error': exception
                }, request=self.request
            )


class AssetEditView(SingleObjectEditView):
    fields = ('label', 'internal_name', 'file')
    model = Asset
    object_permission = permission_asset_edit
    pk_url_kwarg = 'asset_id'
    post_action_redirect = reverse_lazy(viewname='converter:asset_list')

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _('Edit asset: %s') % self.object,
        }


class AssetListView(SingleObjectListView):
    model = Asset
    object_permission = permission_asset_view

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_asset_list,
            'no_results_main_link': link_asset_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Assets are files that can be used in conjuction with '
                'certain transformations.'
            ),
            'no_results_title': _('No assets available'),
            'title': _('Assets'),
        }


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
            messages.error(
                message=_('Error creating transformation: %s.') % exception,
                request=self.request
            )
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
            'initial': {'order': None},
            'transformation_name': self.kwargs['transformation_name']
        }

    def get_external_object_permission(self):
        return self.layer.get_permission(action='create')

    def get_post_action_redirect(self):
        return reverse(
            viewname='converter:transformation_list', kwargs={
                'app_label': self.kwargs['app_label'],
                'model_name': self.kwargs['model_name'],
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
    pk_url_kwarg = 'transformation_id'

    def get_extra_context(self):
        return {
            'content_object': self.object.object_layer.content_object,
            'layer_name': self.layer.name,
            'navigation_object_list': ('content_object', 'transformation'),
            'previous': self.get_post_action_redirect(),
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
        return self.layer.get_permission(action='delete')

    def get_post_action_redirect(self):
        return reverse(
            viewname='converter:transformation_list', kwargs={
                'app_label': self.object.object_layer.content_type.app_label,
                'model_name': self.object.object_layer.content_type.model,
                'object_id': self.object.object_layer.object_id,
                'layer_name': self.object.object_layer.stored_layer.name
            }
        )


class TransformationEditView(LayerViewMixin, SingleObjectEditView):
    form_class = LayerTransformationForm
    model = LayerTransformation
    pk_url_kwarg = 'transformation_id'

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
        return self.layer.get_permission(action='edit')

    def get_post_action_redirect(self):
        return reverse(
            viewname='converter:transformation_list', kwargs={
                'app_label': self.object.object_layer.content_type.app_label,
                'model_name': self.object.object_layer.content_type.model,
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
        return self.layer.get_permission(action='view')

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
    LayerViewMixin, ExternalContentTypeObjectMixin, FormView
):
    form_class = LayerTransformationSelectForm
    template_name = 'appearance/generic_form.html'

    def form_valid(self, form):
        transformation_class = BaseTransformation.get(
            name=form.cleaned_data['transformation']
        )
        if transformation_class.arguments:
            return HttpResponseRedirect(
                redirect_to=reverse(
                    viewname='converter:transformation_create',
                    kwargs={
                        'app_label': self.kwargs['app_label'],
                        'model_name': self.kwargs['model_name'],
                        'object_id': self.kwargs['object_id'],
                        'layer_name': self.kwargs['layer_name'],
                        'transformation_name': form.cleaned_data[
                            'transformation'
                        ]
                    }
                )
            )
        else:
            layer = self.layer
            content_type = self.get_content_type()
            object_layer, created = ObjectLayer.objects.get_or_create(
                content_type=content_type, object_id=self.external_object.pk,
                stored_layer=layer.stored_layer
            )
            object_layer.transformations.create(
                name=form.cleaned_data['transformation']
            )

            messages.success(
                message=_('Transformation created successfully.'),
                request=self.request
            )

            return HttpResponseRedirect(
                redirect_to=reverse(
                    viewname='converter:transformation_list', kwargs={
                        'app_label': self.kwargs['app_label'],
                        'model_name': self.kwargs['model_name'],
                        'object_id': self.kwargs['object_id'],
                        'layer_name': self.kwargs['layer_name']
                    }
                )
            )

    def get_external_object_permission(self):
        return self.layer.get_permission(action='select')

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
