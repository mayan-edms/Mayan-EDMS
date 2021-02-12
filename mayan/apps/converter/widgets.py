from django import forms


class AssetImageWidget(forms.widgets.Widget):
    template_name = 'converter/forms/widgets/asset_image.html'

    def format_value(self, value):
        if value == '' or value is None:
            return None
        return value
