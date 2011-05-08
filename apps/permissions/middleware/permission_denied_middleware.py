from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.template import RequestContext, Template, loader, TemplateDoesNotExist
from django.utils.importlib import import_module


#http://mitchfournier.com/2010/07/12/show-a-custom-403-forbidden-error-page-in-django/
class PermissionDeniedMiddleware(object):
    def process_exception(self, request, exception):
        if isinstance(exception, PermissionDenied):
            try:
                # Handle import error but allow any type error from view
                callback = getattr(import_module(settings.ROOT_URLCONF), u'handler403')
                return callback(request, exception)
            except (ImportError, AttributeError):
                # Try to get a 403 template
                try:
                    # First look for a user-defined template named "403.html"
                    t = loader.get_template(u'403.html')
                except TemplateDoesNotExist:
                    # If a template doesn't exist in the projct, use the following hardcoded template
                    t = Template(u'''{% load i18n %}
                     <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
                            "http://www.w3.org/TR/html4/strict.dtd">
                     <html>
                     <head>
                         <title>{% trans "403 ERROR: Access denied" %}</title>
                     </head>
                     <body>
                         <h1>{% trans "Access Denied (403)" %}</h1>
                         {% trans "We're sorry, but you are not authorized to view this page." %}
                     </body>
                     </html>''')

                # Now use context and render template
                c = RequestContext(request)

                return HttpResponseForbidden(t.render(c))
