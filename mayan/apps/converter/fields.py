from PIL import Image
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import CircleModuleDrawer

from django import forms
from django.contrib.staticfiles.storage import staticfiles_storage

from .widgets import AssetImageWidget, Base64ImageWidget

LOGO_PATH = 'converter/images/logo.png'


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

        with staticfiles_storage.open(name=LOGO_PATH, mode='rb') as file_object:
            embeded_image = Image.open(fp=file_object)

            qrcode_image = instance.make_image(
                image_factory=StyledPilImage,
                module_drawer=CircleModuleDrawer(),
                embeded_image=embeded_image
            )

            size = qrcode_image.height / 2

            self.widget.attrs['height'] = size
            self.widget.attrs['width'] = size

            return qrcode_image
