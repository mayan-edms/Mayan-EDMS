from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils import timezone, translation
from django.utils.translation import ugettext_lazy as _

from mayan.apps.user_management.permissions import (
    permission_user_edit, permission_user_view
)
from mayan.apps.user_management.querysets import get_user_queryset
from mayan.apps.views.generics import (
    SingleObjectDetailView, SingleObjectEditView
)

from .forms import LocaleProfileForm, LocaleProfileForm_view


class UserLocaleProfileDetailView(SingleObjectDetailView):
    form_class = LocaleProfileForm_view
    #model = get_user_model()
    pk_url_kwarg = 'user_id'

    def get_extra_context(self, **kwargs):
        return {
            'form': LocaleProfileForm_view(
                instance=self.object.locale_profile
            ),
            'object': self.object,
            'read_only': True,
            'title': _('Locale profile for user: %s') % self.object
        }

    def get_object_permission(self):
        if self.get_object == self.request.user:
            return
        else:
            return permission_user_view

    def get_source_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return get_user_model().objects.all()
        else:
            return get_user_queryset()


class UserLocaleProfileEditView(SingleObjectEditView):
    form_class = LocaleProfileForm
    #model = get_user_model()
    pk_url_kwarg = 'user_id'

    def form_valid(self, form):
        form.save()

        if self.object == self.request.user:
            timezone.activate(timezone=form.cleaned_data['timezone'])
            translation.activate(language=form.cleaned_data['language'])

            if hasattr(self.request, 'session'):
                self.request.session[
                    translation.LANGUAGE_SESSION_KEY
                ] = form.cleaned_data['language']
                self.request.session[
                    settings.TIMEZONE_SESSION_KEY
                ] = form.cleaned_data['timezone']
            else:
                self.request.set_cookie(
                    settings.LANGUAGE_COOKIE_NAME, form.cleaned_data['language']
                )
                self.request.set_cookie(
                    settings.TIMEZONE_COOKIE_NAME, form.cleaned_data['timezone']
                )

        return super().form_valid(form=form)

    def get_extra_context(self, **kwargs):
        return {
            'object': self.object,
            'title': _('Edit locale profile for user: %s') % self.object
        }

    def get_object_permission(self):
        if self.get_object == self.request.user:
            return
        else:
            return permission_user_edit

    def get_source_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return get_user_model().objects.all()
        else:
            return get_user_queryset()
