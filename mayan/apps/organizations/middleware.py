from .models import Organization


class CurrentOrganizationMiddleware(object):
    """
    Middleware that sets `organization` attribute to request object.
    """

    def process_request(self, request):
        request.organization = Organization.objects.get_current()
