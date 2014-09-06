from django.utils.translation import ugettext_lazy as _

search = {'text': _(u'search'), 'view': 'search:search', 'famfam': 'zoom'}
search_advanced = {'text': _(u'advanced search'), 'view': 'search:search_advanced', 'famfam': 'zoom_in'}
search_again = {'text': _(u'search again'), 'view': 'search:search_again', 'famfam': 'arrow_undo'}
search_menu = {'text': _(u'search'), 'view': 'search:search', 'famfam': 'zoom', 'children_view_regex': [r'^search:']}
