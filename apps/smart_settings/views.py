from __future__ import absolute_import

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from common.utils import return_type, encapsulate
from common.widgets import exists_with_famfam
from navigation import Link
from app_registry.models import App

from .classes import SettingsNamespace
from .links import is_superuser
from .icons import icon_settings


def setting_list(request, app_name=None, object_list=None, title=None, extra_context=None):
    #TODO: check user is super user
    namespace_links = []

    for app in App.live.filter(name__in=[namespace.name for namespace in SettingsNamespace.get_all()]):
        namespace_links.append(
            Link(text=app.label, view='setting_list', args=[u'"%s"' % app.name], icon=getattr(app, 'icon') or icon_settings, condition=is_superuser, children_view_regex=[r'^setting_'])
        )

    if app_name:
        app = get_object_or_404(App, name=app_name)
        selected_namespace = SettingsNamespace.get(app_name)
        app_settings = selected_namespace.get_settings()
        title = _(u'settings for the app: %s') % app_name
    else:
        object_list = []

    context = {
        'title': title if title else _(u'settings'),
        'object_list': object_list if not (object_list is None) else [setting for setting in selected_namespace.get_settings() if setting.hidden == False],
        'hide_link': True,
        'hide_object': True,
        'extra_columns': [
            {'name': _(u'name'), 'attribute': encapsulate(lambda x: mark_safe(u'<span style="font-weight: bold;">%s</span><br />%s' % (x.name, x.description or u'')))},
            {'name': _(u'scopes'), 'attribute': 'get_scopes_display'},
            {'name': _(u'default'), 'attribute': encapsulate(lambda x: return_type(x.default))},
            {'name': _(u'value'), 'attribute': encapsulate(lambda x: mark_safe(u'<div class="nowrap">%s&nbsp;%s</div>' % (
                    return_type(getattr(x.module, x.name)),
                    exists_with_famfam(getattr(x.module, x.name)) if x.exists else ''
                )))
            },
        ],
        'temporary_navigation_links': {
            'form_header': {
                'setting_list': {
                    'links': namespace_links
                },
            }
        }
    }

    if extra_context:
        context.update(extra_context)

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))
