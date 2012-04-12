from __future__ import absolute_import

import datetime

from django.shortcuts import render_to_response
from django.utils.translation import ugettext_lazy as _

from haystack.views import SearchView

from .models import RecentSearch


class CustomSearchView(SearchView):
    def __call__(self, *args, **kwargs):
        self.start_time = datetime.datetime.now()

        return super(CustomSearchView, self).__call__(*args, **kwargs)

    def create_response(self):
        """
        Generates the actual HttpResponse to send back to the user.
        """
        context = {
            'query': self.query,
            'form': self.form,
            'results': self.results,
            'object_list': self.results,
            'suggestion': None,
            'submit_label': _(u'Search'),
            'submit_icon_famfam': 'zoom',
            'form_title': _(u'Search'),
            'form_hide_required_text': True,
            'list_title': _(u'results for: %s') % self.query,
            'hide_links': True,
            'multi_select_as_buttons': True,
            'elapsed_time': unicode(datetime.datetime.now() - self.start_time).split(':')[2],
            'object_list_object_name': 'object',
        }

        RecentSearch.objects.add_query_for_user(self)

        context.update(self.extra_context())
        return render_to_response(self.template, context, context_instance=self.context_class(self.request))
