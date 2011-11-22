from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils.http import urlencode

from converter.exceptions import UnknownFileFormat, UnkownConvertError


def document_thumbnail(document):
    return document_html_widget(document, click_view='document_preview')


def document_link(document):
    return mark_safe(u'<a href="%s">%s</a>' % (reverse('document_view_simple', args=[document.pk]), document))


def document_html_widget(document, size='document_thumbnail', click_view=None, page=None, zoom=None, rotation=None, gallery_name=None, fancybox_class='fancybox'):
    result = []
                       
    alt_text = _(u'document page image')
    query_dict = {}
    
    if page:
        query_dict['page'] = page
                       
    if zoom:
        query_dict['zoom'] = zoom

    if rotation:
        query_dict['rotation'] = rotation

    if gallery_name:
        gallery_template = u'rel="%s"' % gallery_name
    else:
        gallery_template = u''
    
    query_string = urlencode(query_dict)
    preview_view = u'%s?%s' % (reverse(size, args=[document.pk]), query_string)
    print 'preview_view', preview_view

    zoomable_template = []
    if click_view:
        zoomable_template.append(u'<a %s class="%s" href="%s">' % (gallery_template, fancybox_class, u'%s?%s' % (reverse(click_view, args=[document.pk]), query_string)))
    zoomable_template.append(u'<img style="border: 1px solid black;" class="lazy-load" data-href="%s" src="%s/images/ajax-loader.gif" alt="%s" />' % (preview_view, settings.STATIC_URL, alt_text))
    zoomable_template.append(u'<noscript><img style="border: 1px solid black;" src="%s" alt="%s" /></noscript>' % (preview_view, alt_text))
    if click_view:
        zoomable_template.append(u'</a>')
    
    """
    plain_template = []
    plain_template.append(u'<img class="lazy-load" data-href="%s" src="%simages/ajax-loader.gif" alt="%s" />' % (preview_view, settings.STATIC_URL, alt_text))
    plain_template.append(u'<noscript><img src="%s" alt="%s" /></noscript>' % (preview_view, alt_text))

    result.append(u'''
        <script type="text/javascript">
        $(document).ready(function() {

            $.get('%(url)s', function(data) {})
                .success(function(data) {
                    if (data.result) {
                        $('#document-%(pk)d-%(page)d').html('%(zoomable_template)s');
                    } else {
                    
                        $('#document-%(pk)d-%(page)d').html('%(plain_template)s');
                    }
                    //$('.fancybox-noscaling').live('click', function(e) {alert("CLICK");});

                })
                .error(function(data) { alert("error"); })
            ;
            });
        </script>
    ''' % {
            u'url': reverse('documents-expensive-is_zoomable', args=[document.pk]),
            u'pk': document.pk,
            u'page': page if page else 1,
            u'zoomable_template': mark_safe(u''.join(zoomable_template)),
            u'plain_template': mark_safe(u''.join(plain_template)),
        }
    )
    
    result.append(u'<div class="tc" id="document-%d-%d">' % (document.pk, page if page else 1))
    result.append(u'<a href="%s">' % (u'%s?%s' % (reverse(click_view, args=[document.pk]), query_string)))
    result.append(u'<img src="%s/images/ajax-loader.gif" alt="%s" />' % (settings.STATIC_URL, alt_text))
    result.append(u'<noscript><img style="border: 1px solid black;" src="%s" alt="%s" /></noscript>' % (preview_view, alt_text))
    result.append(u'</a>')
    result.append(u'</div>')
    """
    
    #Fancybox w/ jQuery live
    """
    jQuery("a.fancybox-noscaling").live('click', function(){
        jQuery.fancybox({
            'autoDimensions'  : false,
            'width'           : 'auto',
            'height'          : 'auto',
            'href'            : $(this).attr('href'),
                'titleShow'     : false,
                'transitionIn'  : 'elastic',
                'transitionOut' : 'elastic',
                'easingIn'      : 'easeOutBack',
                'easingOut'     : 'easeInBack',
                'type'          : 'image',
                'autoScale'     : false        
            
        });
        return false;
    });    
    """
    result.append(u'<div class="tc" id="document-%d-%d">' % (document.pk, page if page else 1))
    result.extend(zoomable_template)
    result.append(u'</div>')

    return mark_safe(u''.join(result))
