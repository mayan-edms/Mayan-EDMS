from __future__ import absolute_import

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from common.utils import encapsulate
from permissions.models import Permission

from .models import App
from .icons import icon_app


def app_list(request):
    #order =  [i for i,f in sorted(smart_modules.items(), key=lambda k: 'dependencies' in k[1] and k[1]['dependencies'])]

    return render_to_response('generic_list.html', {
        'object_list': App.live.all(),
        'hide_object': True,
        'title': _(u'registered apps'),
        'extra_columns': [
            {'name': _(u'label'), 'attribute': 'label'},
            {'name': _(u'icon'), 'attribute': encapsulate(lambda x: (getattr(x, 'icon') or icon_app).display_big())},
            {'name': _(u'description'), 'attribute': 'description'},
            {'name': _(u'dependencies'), 'attribute': encapsulate(lambda x: u', '.join([unicode(dependency) for dependency in x.dependencies.all()]))},
        ],
    }, context_instance=RequestContext(request))
