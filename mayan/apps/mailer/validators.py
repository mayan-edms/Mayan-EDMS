from django.core import validators
from django.utils.translation import ugettext_lazy as _

from .utils import split_recipient_list


def validate_email_multiple(value):
    recipient_list = split_recipient_list(recipients=[value])

    for recipient in recipient_list:
        validate_email = validators.EmailValidator(
            message=_('%(email)s is not a valid email address.') % {
                'email': recipient
            }
        )
        validate_email(value=recipient)
