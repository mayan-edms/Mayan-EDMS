from __future__ import absolute_import

import datetime

from django.shortcuts import render_to_response
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import PermissionDenied

from haystack.views import SearchView

from documents.permissions import PERMISSION_DOCUMENT_VIEW
from permissions.models import Permission
from acls.models import AccessEntry

from .models import RecentSearch
from .icons import icon_search


class CustomSearchView(SearchView):
    def __call__(self, *args, **kwargs):
        self.start_time = datetime.datetime.now()

        return super(CustomSearchView, self).__call__(*args, **kwargs)

    def create_response(self):
        """
        Generates the actual HttpResponse to send back to the user.
        """
        object_list = self.results.values_list('object', flat=True)
        
        try:
            Permission.objects.check_permissions(self.request.user, [PERMISSION_DOCUMENT_VIEW])
        except PermissionDenied:
            if self.query:
                object_list = AccessEntry.objects.filter_objects_by_access(PERMISSION_DOCUMENT_VIEW, self.request.user, object_list)

        context = {
            'query': self.query,
            'form': self.form,
            'object_list': object_list,
            'suggestion': None,
            'submit_label': _(u'Search'),
            'submit_icon': icon_search,
            'form_title': _(u'Search'),
            'form_hide_required_text': True,
            'list_title': _(u'results for: %s') % self.query,
            'hide_links': True,
            'multi_select_as_buttons': True,
            'elapsed_time': unicode(datetime.datetime.now() - self.start_time).split(':')[2],
        }

        RecentSearch.objects.add_query_for_user(self)

        context.update(self.extra_context())
        return render_to_response(self.template, context, context_instance=self.context_class(self.request))
