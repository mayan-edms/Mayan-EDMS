from __future__ import unicode_literals

from django.utils.html import strip_spaces_between_tags


class SpacelessMiddleware(object):
    """
    Remove spaces between tags in HTML responses to save on bandwidth
    """

    def process_response(self, request, response):
        if 'text/html' in response.get('Content-Type', ''):
            response.content = strip_spaces_between_tags(response.content)
        return response
