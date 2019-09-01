from __future__ import unicode_literals

from django import forms


class ControlSheetCodeImageWidget(forms.widgets.Widget):
    template_name = 'control_codes/forms/widgets/control_sheet_code_image.html'

    def format_value(self, value):
        if value == '' or value is None:
            return None
        return value
