from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages


from permissions.api import check_permissions, Unauthorized


from filesystem_serving import FILESYSTEM_SERVING_RECREATE_LINKS
from api import do_recreate_all_links


def recreate_all_links(request):
    permissions = [FILESYSTEM_SERVING_RECREATE_LINKS]
    try:
        check_permissions(request.user, 'filesystem_serving', permissions)
    except Unauthorized, e:
        raise Http404(e)

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    
    if request.method != 'POST':
        return render_to_response('generic_confirm.html', {
            'previous':previous,
            'next':next,
            'message':_(u'On large databases this operation may take some time to execute.'),
        }, context_instance=RequestContext(request))
    else:     
        try:
            errors, warnings = do_recreate_all_links()
            messages.success(request, _(u'Filesystem links re-creation completed successfully.'))
            for warning in warnings:
                messages.warning(request, warning)
                
        except Exception, e:
            messages.error(request, _(u'Filesystem links re-creation error: %s') % e)
            
        return HttpResponseRedirect(next)
