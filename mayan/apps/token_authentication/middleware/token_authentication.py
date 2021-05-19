import logging

from django.contrib import auth
from django.utils.deprecation import MiddlewareMixin

from .literals import TOKEN_URL_LITERAL

logger = logging.getLogger(name=__name__)


class TokenAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            logger.debug('attempting token authentication')

            token = request.GET.get(
                TOKEN_URL_LITERAL, request.POST.get(
                    TOKEN_URL_LITERAL, None
                )
            )

            user = auth.authenticate(request=request, token=token)

            logger.debug('valid token for user: %s', user)

            if user:
                request.user = user
                auth.login(request, user)
