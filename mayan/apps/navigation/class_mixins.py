import logging

from django.template import Variable, VariableDoesNotExist

logger = logging.getLogger(name=__name__)


class TemplateObjectMixin:
    def check_condition(self, context, resolved_object=None):
        """
        Check to see if menu has a conditional display function and return
        the result of the condition function against the context.
        """
        if self.condition:
            return self.condition(
                context=context, resolved_object=resolved_object
            )
        else:
            return True

    def get_request(self, context, request=None):
        if not request:
            # Try to get the request object the faster way and fallback to
            # the slower method.
            try:
                request = context.request
            except AttributeError:
                # Simple request extraction failed. Might not be a view
                # context. Try alternate method.
                try:
                    request = Variable(var='request').resolve(context=context)
                except VariableDoesNotExist:
                    # There is no request variable, most probable a 500 in
                    # a test view. Don't return any resolved links then.
                    logger.warning(
                        'No request variable, aborting `{}` '
                        'resolution'.format(self.__class__.__name__)
                    )
                    raise

        return request
