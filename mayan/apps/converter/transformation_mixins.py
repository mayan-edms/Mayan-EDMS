import logging

from PIL import Image, ImageColor, ImageDraw

from django import forms
from django.apps import apps
from django.utils.encoding import force_bytes
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.forms import Form
from mayan.apps.views.widgets import ColorWidget

logger = logging.getLogger(name=__name__)


class ImagePasteTransformationMixin:
    class Form(Form):
        rotation = forms.IntegerField(
            help_text=_(
                'Number of degrees to rotate the image counter clockwise '
                'around its center.'
            ), label=_('Rotation'), required=False
        )
        transparency = forms.FloatField(
            help_text=_('Opacity level of the image in percent'),
            label=_('Transparency'), required=False
        )
        zoom = forms.FloatField(
            help_text=_('Zoom level in percent.'), label=_('Zoom'),
            required=False
        )

    @classmethod
    def get_arguments(cls):
        arguments = super().get_arguments() + (
            'rotation', 'transparency', 'zoom'
        )
        return arguments

    def _update_hash(self):
        result = super()._update_hash()
        instance = self.get_model_instance()
        # Add the image hash to the transformation hash. Ensures
        # that the content object image is updated if the image is
        # updated even if the transformation itself is not updated.
        result.update(
            force_bytes(
                s=instance.get_hash()
            )
        )

        return result

    def execute_on(self, *args, **kwargs):
        super().execute_on(*args, **kwargs)
        return self._execute_on(self, *args, **kwargs)

    def get_images(self):
        try:
            self.transparency = float(self.transparency or '100.0')
        except ValueError:
            self.transparency = 100

        if self.transparency < 0:
            self.transparency = 0
        elif self.transparency > 100:
            self.transparency = 100

        try:
            self.rotation = int(self.rotation or '0') % 360
        except ValueError:
            self.rotation = 0

        try:
            self.zoom = float(self.zoom or '100.0')
        except ValueError:
            self.zoom = 100.0

        instance = self.get_model_instance()

        instance_image = instance.get_image()

        if instance_image.mode != 'RGBA':
            instance_image.putalpha(alpha=255)

        instance_image = instance_image.rotate(
            angle=360 - self.rotation, resample=Image.BICUBIC,
            expand=True
        )

        if self.zoom != 100.0:
            zoom_decimal_value = self.zoom / 100.0
            instance_image = instance_image.resize(
                size=(
                    int(instance_image.size[0] * zoom_decimal_value),
                    int(instance_image.size[1] * zoom_decimal_value)
                ), resample=Image.ANTIALIAS
            )

        paste_mask = instance_image.getchannel(channel='A').point(
            lut=lambda pixel: int(pixel * self.transparency / 100)
        )

        return {
            'instance_image': instance_image, 'paste_mask': paste_mask
        }


class ImagePasteCoordinatesAbsoluteTransformationMixin(ImagePasteTransformationMixin):
    arguments = ('left', 'top')
    label = _('Paste an image')
    name = 'paste_image'

    class Form(ImagePasteTransformationMixin.Form):
        left = forms.IntegerField(
            help_text=_('Horizontal position in pixels from the left.'),
            label=_('Left'), required=False
        )
        top = forms.IntegerField(
            help_text=_('Vertical position in pixels from the top.'),
            label=_('Top'), required=False
        )

    def _execute_on(self, *args, **kwargs):
        try:
            self.left = int(self.left or '0')
        except ValueError:
            self.left = 0

        try:
            self.top = int(self.top or '0')
        except ValueError:
            self.top = 0

        if self.left < 0:
            self.left = 0

        if self.top < 0:
            self.top = 0

        images = self.get_images()

        self.image.paste(
            im=images['instance_image'], box=(self.left, self.top),
            mask=images['paste_mask']
        )

        return self.image


class ImagePasteCoordinatesPercentTransformationMixin(ImagePasteTransformationMixin):
    arguments = ('left', 'top')
    label = _('Paste an image (percents coordinates)')
    name = 'paste_image_percent'

    class Form(ImagePasteTransformationMixin.Form):
        left = forms.FloatField(
            help_text=_('Horizontal position in percent from the left.'),
            label=_('Left'), required=False
        )
        top = forms.FloatField(
            help_text=_('Vertical position in percent from the top.'),
            label=_('Top'), required=False
        )

    def _execute_on(self, *args, **kwargs):
        try:
            self.left = float(self.left or '0')
        except ValueError:
            self.left = 0

        try:
            self.top = float(self.top or '0')
        except ValueError:
            self.top = 0

        if self.left < 0:
            self.left = 0

        if self.left > 100:
            self.left = 100

        if self.top < 0:
            self.top = 0

        if self.top > 100:
            self.top = 100

        images = self.get_images()

        base_width, base_height = self.image.size
        image_width, image_height = images['instance_image'].size

        self.left = int(
            self.left / 100.0 * (base_width - image_width)
        )
        self.top = int(
            self.top / 100.0 * (base_height - image_height)
        )

        self.image.paste(
            im=images['instance_image'], box=(self.left, self.top),
            mask=images['paste_mask']
        )

        return self.image


class ImageWatermarkPercentTransformationMixin(ImagePasteTransformationMixin):
    arguments = (
        'left', 'top', 'right', 'bottom', 'horizontal_increment',
        'vertical_increment'
    )
    label = _('Paste an asset as watermark')
    name = 'paste_asset_watermark'

    class Form(ImagePasteTransformationMixin.Form):
        left = forms.IntegerField(
            help_text=_('Horizontal start position in pixels from the left.'),
            label=_('Left'), required=False
        )
        right = forms.IntegerField(
            help_text=_('Horizontal end position in pixels from the right.'),
            label=_('Right'), required=False
        )
        top = forms.IntegerField(
            help_text=_('Vertical start position in pixels from the top.'),
            label=_('Top'), required=False
        )
        bottom = forms.IntegerField(
            help_text=_('Vertical end position in pixels from the top.'),
            label=_('Bottom'), required=False
        )
        horizontal_increment = forms.IntegerField(
            help_text=_('Horizontal position increments in pixels.'),
            label=_('Horizontal increment'), required=False
        )
        vertical_increment = forms.IntegerField(
            help_text=_('Vertical position increments in pixels.'),
            label=_('Vertical increment'), required=False
        )

    def _execute_on(self, *args, **kwargs):
        try:
            self.left = int(self.left or '0')
        except ValueError:
            self.left = 0

        try:
            self.top = int(self.top or '0')
        except ValueError:
            self.top = 0

        try:
            self.right = int(self.right or '0')
        except ValueError:
            self.right = 0

        try:
            self.bottom = int(self.bottom or '0')
        except ValueError:
            self.bottom = 0

        images = self.get_images()

        try:
            self.horizontal_increment = int(self.horizontal_increment or '0')
        except ValueError:
            self.horizontal_increment = 0

        try:
            self.vertical_increment = int(self.vertical_increment or '0')
        except ValueError:
            self.vertical_increment = 0

        if self.horizontal_increment == 0:
            self.horizontal_increment = images['paste_mask'].size[0]

        if self.vertical_increment == 0:
            self.vertical_increment = images['paste_mask'].size[1]

        for x in range(self.left, self.right or self.image.size[0], self.horizontal_increment):
            for y in range(self.top, self.bottom or self.image.size[1], self.vertical_increment):
                self.image.paste(
                    im=images['instance_image'], box=(x, y),
                    mask=images['paste_mask']
                )

        return self.image


class AssetTransformationMixin:
    @classmethod
    def get_form_class(cls):
        SuperForm = super().get_form_class()

        class FormWithSuperArguments(SuperForm):
            asset_name = forms.ChoiceField(
                help_text=_('Asset name'), label=_('Asset'),
                required=True
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

        return FormWithSuperArguments

    @classmethod
    def get_arguments(cls):
        arguments = super().get_arguments() + (
            'asset_name',
        )
        return arguments

    def get_model_instance(self):
        asset_name = getattr(self, 'asset_name', None)

        Asset = apps.get_model(app_label='converter', model_name='Asset')

        try:
            asset = Asset.objects.get(internal_name=asset_name)
        except Asset.DoesNotExist:
            logger.error('Asset "%s" not found.', asset_name)
            raise
        else:
            return asset


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
