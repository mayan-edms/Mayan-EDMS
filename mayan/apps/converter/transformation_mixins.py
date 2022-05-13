import logging

from PIL import Image, ImageColor, ImageDraw

from django import forms
from django.apps import apps
from django.utils.encoding import force_bytes
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.forms import Form
from mayan.apps.views.widgets import ColorWidget

logger = logging.getLogger(name=__name__)


class AssetTransformationMixin:
    class Form(Form):
        asset_name = forms.ChoiceField(
            help_text=_('Asset name'), label=_('Asset'),
            required=True
        )
        rotation = forms.IntegerField(
            help_text=_(
                'Number of degrees to rotate the image counter clockwise '
                'around its center.'
            ), label=_('Rotation'), required=False
        )
        transparency = forms.FloatField(
            help_text=_('Opacity level of the asset in percent'),
            label=_('Transparency'), required=False
        )
        zoom = forms.FloatField(
            help_text=_('Zoom level in percent.'), label=_('Zoom'),
            required=False
        )

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            def get_asset_choices():
                queryset = apps.get_model(
                    app_label='converter', model_name='Asset'
                ).objects.all()

                for asset in queryset.all():
                    yield (asset.internal_name, asset)

            self.fields['asset_name'].choices = get_asset_choices()

    @classmethod
    def get_arguments(cls):
        arguments = super().get_arguments() + (
            'asset_name', 'rotation', 'transparency', 'zoom'
        )
        return arguments

    def _update_hash(self):
        result = super()._update_hash()
        asset = self.get_asset()
        # Add the asset image hash to the transformation hash. Ensures
        # that the content object image is updated if the asset image is
        # updated even if the transformation itself is not updated.
        result.update(
            force_bytes(
                s=asset.get_hash()
            )
        )

        return result

    def get_asset(self):
        asset_name = getattr(self, 'asset_name', None)

        Asset = apps.get_model(app_label='converter', model_name='Asset')

        try:
            asset = Asset.objects.get(internal_name=asset_name)
        except Asset.DoesNotExist:
            logger.error('Asset "%s" not found.', asset_name)
            raise
        else:
            return asset

    def get_asset_images(self):
        try:
            transparency = float(self.transparency or '100.0')
        except ValueError:
            transparency = 100

        if transparency < 0:
            transparency = 0
        elif transparency > 100:
            transparency = 100

        try:
            rotation = int(self.rotation or '0') % 360
        except ValueError:
            rotation = 0

        try:
            zoom = float(self.zoom or '100.0')
        except ValueError:
            zoom = 100.0

        asset = self.get_asset()

        image_asset = asset.get_image()

        if image_asset.mode != 'RGBA':
            image_asset.putalpha(alpha=255)

        image_asset = image_asset.rotate(
            angle=360 - rotation, resample=Image.BICUBIC,
            expand=True
        )

        if zoom != 100.0:
            decimal_value = zoom / 100.0
            image_asset = image_asset.resize(
                size=(
                    int(image_asset.size[0] * decimal_value),
                    int(image_asset.size[1] * decimal_value)
                ), resample=Image.ANTIALIAS
            )

        paste_mask = image_asset.getchannel(channel='A').point(
            lut=lambda pixel: int(pixel * transparency / 100)
        )

        return {
            'image_asset': image_asset, 'paste_mask': paste_mask
        }


class TransformationDrawRectangleMixin:
    class Form(Form):
        fillcolor = forms.CharField(
            help_text=_('Color used to fill the rectangle.'),
            label=_('Fill color'), required=False, widget=ColorWidget()
        )
        fill_transparency = forms.IntegerField(
            help_text=_('Opacity level of the fill color in percent'),
            label=_('Fill transparency'), required=False
        )
        outlinecolor = forms.CharField(
            help_text=_('Color used for the outline of the rectangle.'),
            label=_('Outline color'), required=False, widget=ColorWidget()
        )
        outlinewidth = forms.CharField(
            help_text=_('Width in pixels of the rectangle outline.'),
            label=_('Outline width'), required=False
        )

    def _execute_on(self, *args, **kwargs):
        fillcolor_value = getattr(self, 'fillcolor', None)
        if fillcolor_value:
            fill_color = ImageColor.getrgb(color=fillcolor_value)
        else:
            fill_color = (0, 0, 0)

        try:
            fill_transparency = int(
                getattr(self, 'fill_transparency', None) or '0'
            )
        except ValueError:
            fill_transparency = 100
        else:
            if fill_transparency < 0:
                fill_transparency = 0
            elif fill_transparency > 100:
                fill_transparency = 100

        # Convert transparency to opacity. Invert intensity logic, transpose
        # from percent to 8-bit value.
        opacity = int(
            (100 - fill_transparency) / 100 * 255
        )

        fill_color += (opacity,)

        outlinecolor_value = getattr(self, 'outlinecolor', None)
        if outlinecolor_value:
            outline_color = ImageColor.getrgb(color=outlinecolor_value)
        else:
            outline_color = None

        outlinewidth_value = getattr(self, 'outlinewidth', None)
        if outlinewidth_value:
            outline_width = int(outlinewidth_value)
        else:
            outline_width = 0

        draw = ImageDraw.Draw(im=self.image, mode='RGBA')
        draw.rectangle(
            xy=(self.left, self.top, self.right, self.bottom),
            fill=fill_color,
            outline=outline_color, width=outline_width
        )

        return self.image
