import logging

from django.conf import settings
from django.urls import reverse_lazy
from django.utils import timezone, translation
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.generics import SimpleView, SingleObjectEditView

from .forms import LocaleProfileForm, LocaleProfileForm_view

logger = logging.getLogger(name=__name__)


class CurrentUserLocaleProfileDetailsView(SimpleView):
    template_name = 'appearance/generic_form.html'

    def get_extra_context(self, **kwargs):
        return {
            'form': LocaleProfileForm_view(
                instance=self.request.user.locale_profile
            ),
            'read_only': True,
            'title': _('Current user locale profile details'),
        }


class CurrentUserLocaleProfileEditView(SingleObjectEditView):
    extra_context = {
        'title': _('Edit current user locale profile details')
    }
    form_class = LocaleProfileForm
    post_action_redirect = reverse_lazy(
        viewname='locales:current_user_locale_profile_details'
    )

    def form_valid(self, form):
        form.save()

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

    def get_object(self):
        return self.request.user.locale_profile
