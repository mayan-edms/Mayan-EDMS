from django.conf import settings
from django.utils import timezone, translation
from django.utils.translation import ugettext_lazy as _

from mayan.apps.user_management.permissions import (
    permission_user_edit, permission_user_view
)
from mayan.apps.user_management.querysets import get_user_queryset
from mayan.apps.user_management.views.view_mixins import DynamicExternalUserViewMixin
from mayan.apps.views.generics import (
    SingleObjectDetailView, SingleObjectEditView
)
from mayan.apps.views.mixins import ExternalObjectViewMixin

from .forms import LocaleProfileForm, LocaleProfileForm_view


class UserLocaleProfileDetailView(
    DynamicExternalUserViewMixin, ExternalObjectViewMixin,
    SingleObjectDetailView
):
    form_class = LocaleProfileForm_view
    external_object_permission = permission_user_view
    external_object_pk_url_kwarg = 'user_id'

    def get_external_object_queryset(self):
        return get_user_queryset(user=self.request.user)

    def get_extra_context(self, **kwargs):
        return {
            'form': LocaleProfileForm_view(
                instance=self.external_object.locale_profile
            ),
            'object': self.external_object,
            'read_only': True,
            'title': _('Locale profile for user: %s') % self.external_object
        }

    def get_object(self):
        return self.external_object.locale_profile


class UserLocaleProfileEditView(
    DynamicExternalUserViewMixin, ExternalObjectViewMixin,
    SingleObjectEditView
):
    form_class = LocaleProfileForm
    external_object_permission = permission_user_edit
    external_object_pk_url_kwarg = 'user_id'

    def form_valid(self, form):
        if self.is_current_user:
            language_value = form.cleaned_data['language']
            timezone_value = form.cleaned_data['timezone']

            timezone.activate(timezone=timezone_value)
            translation.activate(language=language_value)

            if hasattr(self.request, 'session'):
                self.request.session[
                    translation.LANGUAGE_SESSION_KEY
                ] = language_value
                self.request.session[
                    settings.TIMEZONE_SESSION_KEY
                ] = timezone_value
            else:
                self.request.set_cookie(
                    settings.LANGUAGE_COOKIE_NAME, language_value
                )
                self.request.set_cookie(
                    settings.TIMEZONE_COOKIE_NAME, timezone_value
                )

        return super().form_valid(form=form)

    def get_external_object_queryset(self):
        return get_user_queryset(user=self.request.user)

    def get_extra_context(self):
        return {
            'title': _(
                'Edit locale profile for user: %s'
            ) % self.external_object,
            'object': self.external_object
        }

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}

    def get_object(self):
        return self.external_object.locale_profile
