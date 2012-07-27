from __future__ import absolute_import

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from common.utils import return_type, encapsulate
from common.widgets import exists_with_famfam
from navigation.api import Link

from .api import settings_list, namespace_list, settings, namespaces
from .links import is_superuser


def setting_list(request, namespace_name=None, object_list=None, title=None, extra_context=None):
    #TODO: check user is super user
    namespace_links = []
    for namespace in namespace_list:
        namespace_links.append(
            Link(text=namespace.label, view='setting_list', args=[u'"%s"' % namespace.name], sprite=getattr(namespace, 'sprite') or 'cog', condition=is_superuser, children_view_regex=[r'^setting_'])
        )

    if namespace_name:
        object_list = [setting for setting in settings[namespace_name] if setting.hidden == False]
        title = _(u'settings for the %s module') % namespaces[namespace_name]

    context = {
        'title': title if title else _(u'settings'),
        'object_list': object_list if not (object_list is None) else [setting for setting in settings_list if setting.hidden == False],
        'hide_link': True,
        'hide_object': True,
        'extra_columns': [
            {'name': _(u'name'), 'attribute': encapsulate(lambda x: mark_safe(u'<span style="font-weight: bold;">%s</span><br />%s' % (x.global_name, x.description)))},
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
