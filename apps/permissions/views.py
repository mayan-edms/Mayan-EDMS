from django.utils.translation import ugettext as _
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib import messages
from django.views.generic.list_detail import object_detail, object_list
from django.core.urlresolvers import reverse
from django.views.generic.create_update import create_object, delete_object, update_object
from django.conf import settings

from models import Role
from forms import RoleForm_view

def role_list(request):
    #permissions = [PERMISSION_ROLE_VIEW]
    #try:
    #    check_permissions(request.user, 'permissions', permissions)
    #except Unauthorized, e:
    #    raise Http404(e)
            
    return object_list(
        request,
        queryset=Role.objects.all(),
        template_name='generic_list.html',
        extra_context={
            'title':_(u'roles'),
        },
    )


def role_view(request, role_id):
    #permissions = [PERMISSION_ROLE_VIEW]
    #try:
    #    check_permissions(request.user, 'permissions', permissions)
    #except Unauthorized, e:
    #    raise Http404(e)
            
    role = get_object_or_404(Role, pk=role_id)
    form = RoleForm_view(instance=role)#, extra_fields=[
    #    {'label':_(u'Filename'), 'field':'file_filename'},
    #    {'label':_(u'File extension'), 'field':'file_extension'},
    #    {'label':_(u'File mimetype'), 'field':'file_mimetype'},
    #    {'label':_(u'File mime encoding'), 'field':'file_mime_encoding'},
    #    {'label':_(u'File size'), 'field':lambda x: pretty_size(x.file.storage.size(x.file.path)) if x.exists() else '-'},
    #    {'label':_(u'Exists in storage'), 'field':'exists'},
    #    {'label':_(u'Date added'), 'field':lambda x: x.date_added.date()},
    #    {'label':_(u'Time added'), 'field':lambda x: unicode(x.date_added.time()).split('.')[0]},
    #    {'label':_(u'Checksum'), 'field':'checksum'},
    #    {'label':_(u'UUID'), 'field':'uuid'},
    #    {'label':_(u'Pages'), 'field':lambda x: x.documentpage_set.count()},
    #])

        
    #subtemplates_dict = [
    #        {
    #            'name':'generic_list_subtemplate.html',
    #            'title':_(u'metadata'),
    #            'object_list':document.documentmetadata_set.all(),
    #            'extra_columns':[{'name':_(u'value'), 'attribute':'value'}],
    #            'hide_link':True,
    #        },
    #    ]
    
    #if FILESYSTEM_FILESERVING_ENABLE:
    #    subtemplates_dict.append({
    #        'name':'generic_list_subtemplate.html',
    #        'title':_(u'index links'),
    #        'object_list':document.documentmetadataindex_set.all(),
    #        'hide_link':True})

           
    return render_to_response('generic_detail.html', {
        #'form_list':[{'form':form, 'object':role}],
        'form':form,
        'object':role,
        #'object':role,
        #'subtemplates_dict':subtemplates_dict,
        #'sidebar_subtemplates_dict':sidebar_groups,
    }, context_instance=RequestContext(request))


def role_create(request):
    #permissions = [PERMISSION_ROLE_CREATE]
    #try:
    #    check_permissions(request.user, 'permissions', permissions)
    #except Unauthorized, e:
    #    raise Http404(e)

    #TODO: post_create redirect
    return create_object(request, model=Role, template_name='generic_form.html')
    
def role_delete(request, role_id):
#    permissions = [PERMISSION_DOCUMENT_DELETE]
#    try:
#        check_permissions(request.user, 'documents', permissions)
#    except Unauthorized, e:
#        raise Http404(e)
#            
    #role = get_object_or_404(Role, pk=role_id)
        
    return delete_object(request, model=Role, object_id=role_id, 
        template_name='generic_confirm.html', 
        post_delete_redirect=reverse('role_list'),
        extra_context={
            'delete_view':True,
            #'object':document,
            'object_name':_(u'role'),
        })
