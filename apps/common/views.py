from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType

from common.forms import ChoiceForm


def password_change_done(request):
    """
    View called when the new user password has been accepted
    """

    messages.success(request, _(u'Your password has been successfully changed.'))
    return redirect('home')


def multi_object_action_view(request):
    """
    Proxy view called first when usuing a multi object action, which
    then redirects to the appropiate specialized view
    """

    action = request.GET.get('action', None)
    id_list = u','.join([key[3:] for key in request.GET.keys() if key.startswith('pk_')])

    if not action:
        messages.error(request, _(u'No action selected.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if not id_list:
        messages.error(request, _(u'Must select at least one item.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    return HttpResponseRedirect('%s?id_list=%s' % (action, id_list))


def get_obj_from_content_type_string(string):
    model, pk = string.split(u',')
    ct = ContentType.objects.get(model=model)
    return ct.get_object_for_this_type(pk=pk)


def assign_remove(request, left_list, right_list, add_method, remove_method, left_list_title, right_list_title, obj=None, object_name=None, decode_content_type=False):
    left_list_name = u'left_list'
    right_list_name = u'right_list'

    if request.method == 'POST':
        if u'%s-submit' % left_list_name in request.POST.keys():
            unselected_list = ChoiceForm(request.POST,
                prefix=left_list_name,
                choices=left_list())
            if unselected_list.is_valid():
                for selection in unselected_list.cleaned_data['selection']:
                    label = dict(left_list())[selection]
                    if decode_content_type:
                        selection_obj = get_obj_from_content_type_string(selection)
                    else:
                        selection_obj = selection
                    try:
                        add_method(selection_obj)
                        messages.success(request, _(u'%(selection)s added successfully added to %(right_list_title)s.') % {
                            'selection': label, 'right_list_title': right_list_title})
                    except:
                        messages.error(request, _(u'Unable to add %(selection)s to %(right_list_title)s.') % {
                            'selection': label, 'right_list_title': right_list_title})

        elif u'%s-submit' % right_list_name in request.POST.keys():
            selected_list = ChoiceForm(request.POST,
                prefix=right_list_name,
                choices=right_list())
            if selected_list.is_valid():
                for selection in selected_list.cleaned_data['selection']:
                    label = dict(right_list())[selection]
                    if decode_content_type:
                        selection = get_obj_from_content_type_string(selection)
                    try:
                        remove_method(selection)
                        messages.success(request, _(u'%(selection)s added successfully removed from %(right_list_title)s.') % {
                            'selection': label, 'right_list_title': right_list_title})
                    except:
                        messages.error(request, _(u'Unable to add %(selection)s to %(right_list_title)s.') % {
                            'selection': label, 'right_list_title': right_list_title})
    unselected_list = ChoiceForm(prefix=left_list_name,
        choices=left_list())
    selected_list = ChoiceForm(prefix=right_list_name,
        choices=right_list())

    context = {
        'subtemplates_list': [
            {
                'name':'generic_form_subtemplate.html',
                'grid': 6,
                'context': {
                    'form': unselected_list,
                    'title': left_list_title,
                    'submit_label': _(u'Add'),
                }
            },
            {
                'name':'generic_form_subtemplate.html',
                'grid': 6,
                'grid_clear': True,
                'context': {
                    'form': selected_list,
                    'title': right_list_title,
                    'submit_label': _(u'Remove'),
                }
            },

        ],
    }
    if obj:
        context.update(
            {
                'object': obj
            }
        )

    if object_name:
        context.update(
            {
                'object_name': object_name,
            }
        )

    return render_to_response('generic_form.html', context,
        context_instance=RequestContext(request))
