# Aliasing it for the sake of page size.
from django.utils.html import strip_spaces_between_tags as short


class SpacelessMiddleware(object):
    def process_response(self, request, response):
        if u'text/html' in response['Content-Type']:
            response.content = short(response.content)
        return response
