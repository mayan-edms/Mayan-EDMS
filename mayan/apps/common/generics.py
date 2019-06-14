from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (
    FormView as DjangoFormView, DetailView, TemplateView
)
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import (
    CreateView, DeleteView, FormMixin, ModelFormMixin, UpdateView
)
from django.views.generic.list import ListView

from django_downloadview import (
    TextIteratorIO, VirtualDownloadView, VirtualFile
)
from pure_pagination.mixins import PaginationMixin

from mayan.apps.acls.models import AccessControlList

from .forms import ChoiceForm
from .icons import (
    icon_add_all, icon_confirm_form_cancel, icon_confirm_form_submit,
    icon_remove_all, icon_assign_remove_add,
    icon_assign_remove_remove, icon_sort_down, icon_sort_up
)
from .literals import (
    TEXT_SORT_FIELD_PARAMETER, TEXT_SORT_FIELD_VARIABLE_NAME,
    TEXT_SORT_ORDER_CHOICE_ASCENDING, TEXT_SORT_ORDER_PARAMETER,
    TEXT_SORT_ORDER_VARIABLE_NAME
)
from .mixins import (
    DeleteExtraDataMixin, DynamicFormViewMixin, ExternalObjectMixin,
    ExtraContextMixin, FormExtraKwargsMixin, MultipleObjectMixin,
    ObjectActionMixin, ObjectNameMixin,
    ObjectPermissionCheckMixin, RedirectionMixin, RestrictedQuerysetMixin,
    ViewPermissionCheckMixin
)

from .settings import setting_paginate_by


# Required by other views, moved to the top
class MultiFormView(DjangoFormView):
    prefix = None
    prefixes = {}
    template_name = 'appearance/generic_form.html'

    def _create_form(self, form_name, klass):
        form_kwargs = self.get_form_kwargs(form_name)
        form_create_method = 'create_%s_form' % form_name
        if hasattr(self, form_create_method):
            form = getattr(self, form_create_method)(**form_kwargs)
        else:
            form = klass(**form_kwargs)
        return form

    def all_forms_valid(self, forms):
        return None

    def dispatch(self, request, *args, **kwargs):
        form_classes = self.get_form_classes()
        self.forms = self.get_forms(form_classes)
        return super(MultiFormView, self).dispatch(request, *args, **kwargs)

    def forms_valid(self, forms):
        for form_name, form in forms.items():
            form_valid_method = '%s_form_valid' % form_name

            if hasattr(self, form_valid_method):
                return getattr(self, form_valid_method)(form)

        self.all_forms_valid(forms)

        return HttpResponseRedirect(redirect_to=self.get_success_url())

    def forms_invalid(self, forms):
        return self.render_to_response(self.get_context_data(forms=forms))

    def get_context_data(self, **kwargs):
        """
        Insert the form into the context dict.
        """
        if 'forms' not in kwargs:
            kwargs['forms'] = self.get_forms(
                form_classes=self.get_form_classes()
            )
        return super(FormMixin, self).get_context_data(**kwargs)

    def get_form_classes(self):
        return self.form_classes

    def get_form_kwargs(self, form_name):
        kwargs = {}
        kwargs.update({'initial': self.get_initial(form_name)})
        kwargs.update({'prefix': self.get_prefix(form_name)})

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })

        kwargs.update(self.get_form_extra_kwargs(form_name=form_name) or {})

        return kwargs

    def get_form_extra_kwargs(self, form_name):
        return None

    def get_forms(self, form_classes):
        return dict(
            [
                (
                    key, self._create_form(key, klass)
                ) for key, klass in form_classes.items()
            ]
        )

    def get_initial(self, form_name):
        initial_method = 'get_%s_initial' % form_name
        if hasattr(self, initial_method):
            return getattr(self, initial_method)()
        else:
            return self.initial.copy()

    def get_prefix(self, form_name):
        return self.prefixes.get(form_name, self.prefix)

    def post(self, request, *args, **kwargs):
        if all([form.is_valid() for form in self.forms.values()]):
            return self.forms_valid(forms=self.forms)
        else:
            return self.forms_invalid(forms=self.forms)


class AddRemoveView(
    ExternalObjectMixin, ExtraContextMixin, ViewPermissionCheckMixin,
    RestrictedQuerysetMixin, MultiFormView
):
    form_classes = {'form_available': ChoiceForm, 'form_added': ChoiceForm}
    list_added_help_text = _(
        'Select entries to be removed. Hold Control to select multiple '
        'entries. Once the selection is complete, click the button below '
        'or double click the list to activate the action.'
    )
    list_available_help_text = _(
        'Select entries to be added. Hold Control to select multiple '
        'entries. Once the selection is complete, click the button below '
        'or double click the list to activate the action.'
    )

    # Form titles
    list_added_title = None
    list_available_title = None

    # Attributes to filter the object to which selections will be added or
    # remove
    main_object_model = None
    main_object_permission = None
    main_object_pk_url_kwarg = None
    main_object_pk_url_kwargs = None
    main_object_source_queryset = None

    # Attributes to filter the queryset of the selection
    secondary_object_model = None
    secondary_object_permission = None
    secondary_object_source_queryset = None

    # Main object methods to use to add and remove selections
    main_object_method_add = None
    main_object_method_remove = None

    # If a method is not specified, use this related field to add and remove
    # selections
    related_field = None

    prefixes = {'form_available': 'available', 'form_added': 'added'}

    def __init__(self, *args, **kwargs):
        self.external_object_class = self.main_object_model
        self.external_object_permission = self.main_object_permission
        self.external_object_pk_url_kwarg = self.main_object_pk_url_kwarg
        self.external_object_pk_url_kwargs = self.main_object_pk_url_kwargs
        self.external_object_queryset = self.main_object_source_queryset

        super(AddRemoveView, self).__init__(*args, **kwargs)

    def _action_add(self, queryset):
        kwargs = {'queryset': queryset}
        kwargs.update(self.get_action_add_extra_kwargs())
        kwargs.update(self.get_actions_extra_kwargs())

        if hasattr(self, 'action_add'):
            with transaction.atomic():
                self.action_add(**kwargs)
        elif self.main_object_method_add:
            getattr(self.main_object, self.main_object_method_add)(**kwargs)
        elif self.related_field:
            getattr(self.main_object, self.related_field).add(*queryset)
        else:
            raise ImproperlyConfigured(
                'View %s must be called with a main_object_method_add, a '
                'related_field, or an action_add '
                'method.' % self.__class__.__name__
            )

    def _action_remove(self, queryset):
        kwargs = {'queryset': queryset}
        kwargs.update(self.get_action_remove_extra_kwargs())
        kwargs.update(self.get_actions_extra_kwargs())

        if hasattr(self, 'action_remove'):
            with transaction.atomic():
                self.action_remove(**kwargs)
        elif self.main_object_method_remove:
            getattr(self.main_object, self.main_object_method_remove)(**kwargs)
        elif self.related_field:
            getattr(self.main_object, self.related_field).remove(*queryset)
        else:
            raise ImproperlyConfigured(
                'View %s must be called with a main_object_method_remove, a '
                'related_field, or an action_remove '
                'method.' % self.__class__.__name__
            )

    def dispatch(self, request, *args, **kwargs):
        self.main_object = self.get_external_object()
        result = super(AddRemoveView, self).dispatch(request=request, *args, **kwargs)
        return result

    def forms_valid(self, forms):
        if 'available-add_all' in self.request.POST:
            selection_add = self.get_list_available_queryset()
        else:
            selection_add = self.get_list_available_queryset().filter(
                pk__in=forms['form_available'].cleaned_data['selection']
            )

        self._action_add(queryset=selection_add)

        if 'added-remove_all' in self.request.POST:
            selection_remove = self.get_list_added_queryset()
        else:
            selection_remove = self.get_list_added_queryset().filter(
                pk__in=forms['form_added'].cleaned_data['selection']
            )

        self._action_remove(queryset=selection_remove)

        return super(AddRemoveView, self).forms_valid(forms=forms)

    def generate_choices(self, queryset):
        for obj in queryset:
            yield (obj.pk, force_text(obj))

    def get_action_add_extra_kwargs(self):
        # Keyword arguments to apply to the add method
        return {}

    def get_action_remove_extra_kwargs(self):
        # Keyword arguments to apply to the remove method
        return {}

    def get_actions_extra_kwargs(self):
        # Keyword arguments to apply to both the add and remove methods
        return {}

    def get_context_data(self, **kwargs):
        # Use get_context_data to leave the get_extra_context for subclasses
        context = super(AddRemoveView, self).get_context_data(**kwargs)
        context.update(
            {
                'subtemplates_list': [
                    {
                        'name': 'appearance/generic_form_subtemplate.html',
                        'column_class': 'col-xs-12 col-sm-6 col-md-6 col-lg-6',
                        'context': {
                            'extra_buttons': [
                                {
                                    'label': _('Add all'),
                                    'icon_class': icon_add_all,
                                    'name': 'add_all',
                                }
                            ],
                            'form': self.forms['form_available'],
                            'form_css_classes': 'form-hotkey-double-click',
                            'hide_labels': True,
                            'submit_icon_class': icon_assign_remove_add,
                            'submit_label': _('Add'),
                            'title': self.list_available_title or ' ',
                        }
                    },
                    {
                        'name': 'appearance/generic_form_subtemplate.html',
                        'column_class': 'col-xs-12 col-sm-6 col-md-6 col-lg-6',
                        'context': {
                            'extra_buttons': [
                                {
                                    'label': _('Remove all'),
                                    'icon_class': icon_remove_all,
                                    'name': 'remove_all',
                                }
                            ],
                            'form': self.forms['form_added'],
                            'form_css_classes': 'form-hotkey-double-click',
                            'hide_labels': True,
                            'submit_icon_class': icon_assign_remove_remove,
                            'submit_label': _('Remove'),
                            'title': self.list_added_title or ' ',
                        }
                    }
                ]
            }
        )

        return context

    def get_disabled_choices(self):
        return ()

    def get_form_extra_kwargs(self, form_name):
        if form_name == 'form_available':
            return {
                'choices': self.generate_choices(
                    queryset=self.get_list_available_queryset()
                ),
                'help_text': self.get_list_available_help_text()
            }
        else:
            return {
                'choices': self.generate_choices(
                    queryset=self.get_list_added_queryset()
                ),
                'disabled_choices': self.get_disabled_choices(),
                'help_text': self.get_list_added_help_text()
            }

    def get_list_added_help_text(self):
        return self.list_added_help_text

    def get_list_added_queryset(self):
        if not self.related_field:
            raise ImproperlyConfigured(
                'View %s must be called with either a related_field or '
                'override .get_list_added_queryset().' % self.__class__.__name__
            )

        return self.get_secondary_object_list().filter(
            pk__in=getattr(self.main_object, self.related_field).values('pk')
        )

    def get_list_available_help_text(self):
        return self.list_available_help_text

    def get_list_available_queryset(self):
        return self.get_secondary_object_list().exclude(
            pk__in=self.get_list_added_queryset().values('pk')
        )

    def get_secondary_object_list(self):
        queryset = self.get_secondary_object_source_queryset()

        if queryset is None:
            queryset = self.secondary_object_model._meta.default_manager.all()

        if self.secondary_object_permission:
            return AccessControlList.objects.restrict_queryset(
                permission=self.secondary_object_permission, queryset=queryset,
                user=self.request.user
            )
        else:
            return queryset

    def get_secondary_object_source_queryset(self):
        return self.secondary_object_source_queryset

    def get_success_url(self):
        # Redirect to the same view
        return reverse(
            viewname=self.request.resolver_match.view_name,
            kwargs=self.request.resolver_match.kwargs
        )


class ConfirmView(
    RestrictedQuerysetMixin, ViewPermissionCheckMixin, ExtraContextMixin,
    RedirectionMixin, TemplateView
):
    template_name = 'appearance/generic_confirm.html'

    def get_context_data(self, **kwargs):
        context = {
            'submit_icon_class': icon_confirm_form_submit,
            'cancel_icon_class': icon_confirm_form_cancel
        }
        context.update(super(ConfirmView, self).get_context_data(**kwargs))
        return context

    def post(self, request, *args, **kwargs):
        self.view_action()
        return HttpResponseRedirect(redirect_to=self.get_success_url())


class FormView(
    ViewPermissionCheckMixin, ExtraContextMixin, RedirectionMixin,
    FormExtraKwargsMixin, DjangoFormView
):
    template_name = 'appearance/generic_form.html'


class DynamicFormView(DynamicFormViewMixin, FormView):
    pass


class MultipleObjectFormActionView(
    ExtraContextMixin, ObjectActionMixin, ViewPermissionCheckMixin,
    RestrictedQuerysetMixin, MultipleObjectMixin, FormExtraKwargsMixin,
    RedirectionMixin, DjangoFormView
):
    """
    This view will present a form and upon receiving a POST request will
    perform an action on an object or queryset
    """
    template_name = 'appearance/generic_form.html'

    def __init__(self, *args, **kwargs):
        result = super(MultipleObjectFormActionView, self).__init__(*args, **kwargs)

        if self.__class__.mro()[0].get_queryset != MultipleObjectFormActionView.get_queryset:
            raise ImproperlyConfigured(
                '%(cls)s is overloading the get_queryset method. Subclasses '
                'should implement the get_source_queryset method instead. ' % {
                    'cls': self.__class__.__name__
                }
            )

        return result

    def form_valid(self, form):
        self.view_action(form=form)
        return super(MultipleObjectFormActionView, self).form_valid(form=form)

    def get_queryset(self):
        try:
            return super(MultipleObjectFormActionView, self).get_queryset()
        except ImproperlyConfigured:
            self.queryset = self.get_source_queryset()
            return super(MultipleObjectFormActionView, self).get_queryset()


class MultipleObjectConfirmActionView(
    ExtraContextMixin, ObjectActionMixin, ViewPermissionCheckMixin,
    RestrictedQuerysetMixin, MultipleObjectMixin, RedirectionMixin, TemplateView
):
    template_name = 'appearance/generic_confirm.html'

    def __init__(self, *args, **kwargs):
        result = super(MultipleObjectConfirmActionView, self).__init__(*args, **kwargs)

        if self.__class__.mro()[0].get_queryset != MultipleObjectConfirmActionView.get_queryset:
            raise ImproperlyConfigured(
                '%(cls)s is overloading the get_queryset method. Subclasses '
                'should implement the get_source_queryset method instead. ' % {
                    'cls': self.__class__.__name__
                }
            )

        return result

    def get_queryset(self):
        try:
            return super(MultipleObjectConfirmActionView, self).get_queryset()
        except ImproperlyConfigured:
            self.queryset = self.get_source_queryset()
            return super(MultipleObjectConfirmActionView, self).get_queryset()

    def post(self, request, *args, **kwargs):
        self.view_action()
        return HttpResponseRedirect(redirect_to=self.get_success_url())


class SimpleView(ViewPermissionCheckMixin, ExtraContextMixin, TemplateView):
    pass


class SingleObjectCreateView(
    ObjectNameMixin, ViewPermissionCheckMixin, ExtraContextMixin,
    RedirectionMixin, FormExtraKwargsMixin, CreateView
):
    error_message_duplicate = None
    template_name = 'appearance/generic_form.html'

    def form_valid(self, form):
        # This overrides the original Django form_valid method

        self.object = form.save(commit=False)

        if hasattr(self, 'get_instance_extra_data'):
            for key, value in self.get_instance_extra_data().items():
                setattr(self.object, key, value)

        if hasattr(self, 'get_save_extra_data'):
            save_extra_data = self.get_save_extra_data()
        else:
            save_extra_data = {}

        try:
            self.object.validate_unique()
        except ValidationError as exception:
            raise
            context = self.get_context_data()

            error_message = self.get_error_message_duplicate() or _(
                'Duplicate data error: %(error)s'
            ) % {
                'error': '\n'.join(exception.messages)
            }

            messages.error(
                message=error_message, request=self.request
            )
            return super(
                SingleObjectCreateView, self
            ).form_invalid(form=form)

        try:
            self.object.save(**save_extra_data)
        except Exception as exception:
            raise
            if settings.DEBUG:
                raise
            else:
                context = self.get_context_data()

                messages.error(
                    message=_('%(object)s not created, error: %(error)s') % {
                        'object': self.get_object_name(context=context),
                        'error': exception
                    }, request=self.request
                )
                return super(
                    SingleObjectCreateView, self
                ).form_invalid(form=form)
        else:
            context = self.get_context_data()

            messages.success(
                message=_(
                    '%(object)s created successfully.'
                ) % {'object': self.get_object_name(context=context)},
                request=self.request
            )

        return HttpResponseRedirect(redirect_to=self.get_success_url())

    def get_error_message_duplicate(self):
        return self.error_message_duplicate


class SingleObjectDeleteView(
    ObjectNameMixin, DeleteExtraDataMixin, ViewPermissionCheckMixin,
    RestrictedQuerysetMixin, ExtraContextMixin, RedirectionMixin, DeleteView
):
    template_name = 'appearance/generic_confirm.html'

    def __init__(self, *args, **kwargs):
        result = super(SingleObjectDeleteView, self).__init__(*args, **kwargs)

        if self.__class__.mro()[0].get_queryset != SingleObjectDeleteView.get_queryset:
            raise ImproperlyConfigured(
                '%(cls)s is overloading the get_queryset method. Subclasses '
                'should implement the get_source_queryset method instead. ' % {
                    'cls': self.__class__.__name__
                }
            )

        return result

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        object_name = self.get_object_name(context=context)

        try:
            result = super(SingleObjectDeleteView, self).delete(request, *args, **kwargs)
        except Exception as exception:
            messages.error(
                message=_('%(object)s not deleted, error: %(error)s.') % {
                    'object': object_name,
                    'error': exception
                }, request=self.request
            )
            raise
        else:
            messages.success(
                message=_(
                    '%(object)s deleted successfully.'
                ) % {'object': object_name},
                request=self.request
            )

            return result

    def get_context_data(self, **kwargs):
        context = super(SingleObjectDeleteView, self).get_context_data(**kwargs)
        context.update({'delete_view': True})
        return context

    def get_queryset(self):
        try:
            return super(SingleObjectDeleteView, self).get_queryset()
        except ImproperlyConfigured:
            self.queryset = self.get_source_queryset()
            return super(SingleObjectDeleteView, self).get_queryset()


class SingleObjectDetailView(
    ViewPermissionCheckMixin, RestrictedQuerysetMixin, FormExtraKwargsMixin,
    ExtraContextMixin, ModelFormMixin, DetailView
):
    template_name = 'appearance/generic_form.html'

    def __init__(self, *args, **kwargs):
        result = super(SingleObjectDetailView, self).__init__(*args, **kwargs)

        if self.__class__.mro()[0].get_queryset != SingleObjectDetailView.get_queryset:
            raise ImproperlyConfigured(
                '%(cls)s is overloading the get_queryset method. Subclasses '
                'should implement the get_source_queryset method instead. ' % {
                    'cls': self.__class__.__name__
                }
            )

        return result

    def get_context_data(self, **kwargs):
        context = super(SingleObjectDetailView, self).get_context_data(**kwargs)
        context.update({'read_only': True, 'form': self.get_form()})
        return context

    def get_queryset(self):
        try:
            return super(SingleObjectDetailView, self).get_queryset()
        except ImproperlyConfigured:
            self.queryset = self.get_source_queryset()
            return super(SingleObjectDetailView, self).get_queryset()


class SingleObjectDownloadView(ViewPermissionCheckMixin, ObjectPermissionCheckMixin, VirtualDownloadView, SingleObjectMixin):
    TextIteratorIO = TextIteratorIO
    VirtualFile = VirtualFile


class SingleObjectDynamicFormCreateView(
    DynamicFormViewMixin, SingleObjectCreateView
):
    pass


class SingleObjectEditView(
    ObjectNameMixin, ViewPermissionCheckMixin, RestrictedQuerysetMixin,
    ExtraContextMixin, FormExtraKwargsMixin, RedirectionMixin, UpdateView
):
    template_name = 'appearance/generic_form.html'

    def form_valid(self, form):
        # This overrides the original Django form_valid method

        self.object = form.save(commit=False)

        if hasattr(self, 'get_instance_extra_data'):
            for key, value in self.get_instance_extra_data().items():
                setattr(self.object, key, value)

        if hasattr(self, 'get_save_extra_data'):
            save_extra_data = self.get_save_extra_data()
        else:
            save_extra_data = {}

        context = self.get_context_data()
        object_name = self.get_object_name(context=context)

        try:
            self.object.save(**save_extra_data)
        except Exception as exception:
            if settings.DEBUG:
                raise
            else:
                messages.error(
                    message=_('%(object)s not updated, error: %(error)s.') % {
                        'object': object_name,
                        'error': exception
                    }, request=self.request
                )
                return super(
                    SingleObjectEditView, self
                ).form_invalid(form=form)
        else:
            messages.success(
                message=_(
                    '%(object)s updated successfully.'
                ) % {'object': object_name}, request=self.request
            )

        return HttpResponseRedirect(redirect_to=self.get_success_url())

    def get_object(self, queryset=None):
        obj = super(SingleObjectEditView, self).get_object(queryset=queryset)

        if hasattr(self, 'get_instance_extra_data'):
            for key, value in self.get_instance_extra_data().items():
                setattr(obj, key, value)

        return obj


class SingleObjectDynamicFormEditView(
    DynamicFormViewMixin, SingleObjectEditView
):
    pass


class SingleObjectListView(
    PaginationMixin, ViewPermissionCheckMixin, RestrictedQuerysetMixin,
    ExtraContextMixin, RedirectionMixin, ListView
):
    template_name = 'appearance/generic_list.html'

    def __init__(self, *args, **kwargs):
        result = super(SingleObjectListView, self).__init__(*args, **kwargs)

        if self.__class__.mro()[0].get_queryset != SingleObjectListView.get_queryset:
            raise ImproperlyConfigured(
                '%(cls)s is overloading the get_queryset method. Subclasses '
                'should implement the get_source_queryset method instead. ' % {
                    'cls': self.__class__.__name__
                }
            )

        return result

    def get_context_data(self, **kwargs):
        context = super(SingleObjectListView, self).get_context_data(**kwargs)

        context.update(
            {
                TEXT_SORT_FIELD_VARIABLE_NAME: self.get_sort_field(),
                TEXT_SORT_ORDER_VARIABLE_NAME: self.get_sort_order(),
                'icon_sort': self.get_sort_icon(),
            }
        )
        return context

    def get_paginate_by(self, queryset):
        return setting_paginate_by.value

    def get_queryset(self):
        try:
            queryset = super(SingleObjectListView, self).get_queryset()
        except ImproperlyConfigured:
            self.queryset = self.get_source_queryset()
            queryset = super(SingleObjectListView, self).get_queryset()

        self.field_name = self.get_sort_field()
        if self.get_sort_order() == TEXT_SORT_ORDER_CHOICE_ASCENDING:
            sort_order = ''
        else:
            sort_order = '-'

        if self.field_name:
            queryset = queryset.order_by(
                '{}{}'.format(sort_order, self.field_name)
            )

        return queryset

    def get_sort_field(self):
        return self.request.GET.get(TEXT_SORT_FIELD_PARAMETER)

    def get_sort_icon(self):
        sort_order = self.get_sort_order()
        if not sort_order:
            return
        elif sort_order == TEXT_SORT_ORDER_CHOICE_ASCENDING:
            return icon_sort_down
        else:
            return icon_sort_up

    def get_sort_order(self):
        return self.request.GET.get(TEXT_SORT_ORDER_PARAMETER)
