import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import CircleModuleDrawer

from django import forms

from .widgets import AssetImageWidget, Base64ImageWidget


class AssetImageField(forms.fields.Field):
    widget = AssetImageWidget


class ReadOnlyImageField(forms.ImageField):
    def clean(self, data, initial=None):
        return ''


class QRCodeImageField(ReadOnlyImageField):
    widget = Base64ImageWidget

    def prepare_value(self, value):
        instance = qrcode.QRCode()
        instance.add_data(value)
        instance.make(fit=True)

        qrcode_image = instance.make_image(
            image_factory=StyledPilImage,
            module_drawer=CircleModuleDrawer(),
            embeded_image_path='/tmp/logo.jpg'
        )

        size = qrcode_image.height / 2

        self.widget.attrs['height'] = size
        self.widget.attrs['width'] = size

        return qrcode_image
