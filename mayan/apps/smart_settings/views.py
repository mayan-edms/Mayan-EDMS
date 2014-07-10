from __future__ import absolute_import

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from common.utils import return_type, encapsulate
from common.widgets import exists_with_famfam

from .api import settings


def setting_list(request):
    new_settings = []
    for namespace, sub_settings in settings.items():
        for sub_setting in sub_settings:
            if not sub_setting.get('hidden', False):
                new_settings.append({
                    'module': sub_setting['module'],
                    'name': sub_setting['name'],
                    'global_name': sub_setting['global_name'],
                    'description': sub_setting.get('description', None),
                    'exists': sub_setting.get('exists', False),
                    'default': sub_setting['default'],
                })
    context = {
        'title': _(u'settings'),
        'object_list': new_settings,
        'hide_link': True,
        'hide_object': True,
        'extra_columns': [
            {'name': _(u'name'), 'attribute': encapsulate(lambda x: mark_safe(u'<span style="font-weight: bold;">%s</span><br />%s' % (x.get('global_name'), x.get('description'))))},
            {'name': _(u'default'), 'attribute': encapsulate(lambda x: return_type(x['default']))},
            {
                'name': _(u'value'), 'attribute': encapsulate(lambda x: mark_safe(u'<div class="nowrap">%s&nbsp;%s</div>' % (
                    return_type(getattr(x['module'], x['name'])),
                    exists_with_famfam(getattr(x['module'], x['name'])) if x['exists'] else ''
                )))
            },
        ]
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))
