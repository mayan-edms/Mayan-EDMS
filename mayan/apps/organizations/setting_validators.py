from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validation_fuction_check_path_format(setting, raw_value):
    if raw_value:
        cleaned_raw_value = raw_value.strip()

        if cleaned_raw_value:
            if cleaned_raw_value[0] == '/' or cleaned_raw_value[-1] == '/':
                raise ValidationError(
                    message=_(
                        'The path value must not include a leading or '
                        'trailing slash.'
                    )
                )
            else:
                return cleaned_raw_value
