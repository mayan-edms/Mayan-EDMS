from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import View

from mayan.apps.common.settings import setting_home_view
from mayan.apps.user_management.querysets import get_user_queryset
from mayan.apps.views.http import URL
from mayan.apps.views.generics import FormView
from mayan.apps.views.mixins import (
    ExternalObjectViewMixin, RedirectionViewMixin
)

from ..forms import (
    UserImpersonationOptionsForm, UserImpersonationSelectionForm
)
from ..literals import (
    USER_IMPERSONATE_VARIABLE_ID, USER_IMPERSONATE_VARIABLE_DISABLE,
    USER_IMPERSONATE_VARIABLE_PERMANENT
)
from ..permissions import permission_users_impersonate


class UserImpersonateEndView(RedirectionViewMixin, View):
    def get(self, request, *args, **kwargs):
        url = URL(
            viewname=setting_home_view.value, query={
                USER_IMPERSONATE_VARIABLE_DISABLE: ''
            }
        )
        return HttpResponseRedirect(redirect_to=url.to_string())


class UserImpersonateFormStartView(FormView):
    form_class = UserImpersonationSelectionForm

    def form_valid(self, form):
        query = {
            USER_IMPERSONATE_VARIABLE_ID: form.cleaned_data['user_to_impersonate'].pk
        }
        if form.cleaned_data['permanent']:
            query[USER_IMPERSONATE_VARIABLE_PERMANENT] = ''

        url = URL(
            viewname=setting_home_view.value, query=query
        )
        return HttpResponseRedirect(redirect_to=url.to_string())

    def get_extra_context(self):
        return {
            'title': _('Impersonate user')
        }

    def get_form_extra_kwargs(self):
        return {
            'user': self.request.user
        }


class UserImpersonateStartView(ExternalObjectViewMixin, FormView):
    external_object_queryset = get_user_queryset()
    external_object_permission = permission_users_impersonate
    external_object_pk_url_kwarg = 'user_id'
    form_class = UserImpersonationOptionsForm

    def form_valid(self, form):
        query = {USER_IMPERSONATE_VARIABLE_ID: self.external_object.pk}
        if form.cleaned_data['permanent']:
            query[USER_IMPERSONATE_VARIABLE_PERMANENT] = ''

        url = URL(
            query=query, viewname=setting_home_view.value
        )
        return HttpResponseRedirect(redirect_to=url.to_string())

    def get_extra_context(self):
        return {
            'object': self.external_object,
            'title': _('Impersonate user: %s') % self.external_object
        }
