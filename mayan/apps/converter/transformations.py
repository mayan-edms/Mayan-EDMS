import hashlib
import logging

from PIL import Image, ImageColor, ImageFilter

from django import forms
from django.utils.encoding import force_bytes, force_text
from django.utils.text import format_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.forms import Form
from mayan.apps.views.http import URL
from mayan.apps.views.widgets import ColorWidget

from .layers import layer_decorations, layer_saved_transformations
from .transformation_mixins import (
    AssetTransformationMixin,
    ImagePasteCoordinatesAbsoluteTransformationMixin,
    ImagePasteCoordinatesPercentTransformationMixin,
    ImageWatermarkPercentTransformationMixin,
    TransformationDrawRectangleMixin
)

logger = logging.getLogger(name=__name__)


class BaseTransformationType(type):
    def __str__(self):
        return force_text(s=self.label)


class BaseTransformation(metaclass=BaseTransformationType):
    """
    Transformation can modify the appearance of the document's page preview.
    Some transformation available are: Rotate, zoom, resize and crop.
    """
    arguments = ()
    name = 'base_transformation'
    _layer_transformations = {}
    _registry = {}

    @staticmethod
    def combine(transformations):
        result = hashlib.sha256()

        for transformation in transformations or ():
            try:
                result.update(transformation.cache_hash())
            except Exception as exception:
                logger.error(
                    'Unable to compute hash for transformation: %s; %s',
                    transformation, exception
                )

        return result.hexdigest()

    @staticmethod
    def list_as_query_string(transformation_instance_list):
        result = URL()

        for index, transformation in enumerate(transformation_instance_list):
            result.args['transformation_{}_name'.format(index)] = transformation.name

            for argument in transformation.arguments:
                value = getattr(transformation, argument)
                result.args[
                    'transformation_{}_argument__{}'.format(index, argument)
                ] = value

        return result.to_string()

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def get_arguments(cls):
        return cls.arguments

    @classmethod
    def get_assigned_layer(cls):
        for layer, transformations in cls._layer_transformations.items():
            if cls in transformations:
                return layer

    @classmethod
    def get_form_class(cls):
        return getattr(cls, 'Form', None)

    @classmethod
    def get_label(cls):
        arguments = cls.get_arguments()
        if arguments:
            return format_lazy('{}: {}', cls.label, ', '.join(arguments))
        else:
            return cls.label

    @classmethod
    def get_transformation_choices(cls, group_by_layer=False, layer=None):
        if layer:
            transformation_list = [
                (transformation.name, transformation) for transformation in cls._layer_transformations.get(layer, ())
            ]
        else:
            transformation_list = cls._registry.items()

        if group_by_layer:
            flat_transformation_list = [
                klass for name, klass in transformation_list
            ]

            layer_transformation_choices = {}
            for layer, transformations in cls._layer_transformations.items():
                for transformation in transformations:
                    if transformation in flat_transformation_list:
                        layer_transformation_choices.setdefault(layer, [])
                        layer_transformation_choices[layer].append(
                            (transformation.name, transformation.get_label())
                        )

                # Sort the transformation for each layer group.
                layer_transformation_choices[layer].sort(key=lambda x: x[1])

            result = [
                (layer.label, transformations) for layer, transformations in layer_transformation_choices.items()
            ]

            # Finally sort by transformation layer group.
            return sorted(result, key=lambda x: x[0])
        else:
            return sorted(
                (name, klass.get_label()) for name, klass in transformation_list
            )

    @classmethod
    def register(cls, layer, transformation):
        cls._registry[transformation.name] = transformation
        cls._layer_transformations.setdefault(layer, set())
        cls._layer_transformations[layer].add(transformation)

    def __init__(self, **kwargs):
        self.kwargs = {}
        for argument_name in self.__class__.get_arguments():
            setattr(self, argument_name, kwargs.get(argument_name))
            self.kwargs[argument_name] = kwargs.get(argument_name)

    def _update_hash(self):
        result = hashlib.sha256(force_bytes(s=self.name))

        # Sort arguments for guaranteed repeatability.
        for key, value in sorted(self.kwargs.items()):
            result.update(force_bytes(s=key))
            result.update(force_bytes(s=value))

        return result

    def cache_hash(self):
        return force_bytes(s=self._update_hash().hexdigest())

    def execute_on(self, image):
        self.image = image
        self.aspect = 1.0 * image.size[0] / image.size[1]


class TransformationAssetPaste(
    ImagePasteCoordinatesAbsoluteTransformationMixin,
    AssetTransformationMixin, BaseTransformation
):
    label = _('Paste an asset (absolute coordinates)')
    name = 'paste_asset'


class TransformationAssetPastePercent(
    ImagePasteCoordinatesPercentTransformationMixin,
    AssetTransformationMixin, BaseTransformation
):
    label = _('Paste an asset (percents coordinates)')
    name = 'paste_asset_percent'


class TransformationAssetWatermark(
    ImageWatermarkPercentTransformationMixin, AssetTransformationMixin,
    BaseTransformation
):
    label = _('Paste an asset as watermark')
    name = 'paste_asset_watermark'


class TransformationCrop(BaseTransformation):
    arguments = ('left', 'top', 'right', 'bottom',)
    label = _('Crop')
    name = 'crop'

    class Form(Form):
        left = forms.IntegerField(
            help_text=_('Number of pixels to remove from the left.'),
            label=_('Left'), required=False
        )
        top = forms.IntegerField(
            help_text=_('Number of pixels to remove from the top.'),
            label=_('Top'), required=False
        )
        right = forms.IntegerField(
            help_text=_('Number of pixels to remove from the right.'),
            label=_('Right'), required=False
        )
        bottom = forms.IntegerField(
            help_text=_('Number of pixels to remove from the bottom.'),
            label=_('Bottom'), required=False
        )

    def execute_on(self, *args, **kwargs):
        super().execute_on(*args, **kwargs)

        try:
            left = int(self.left or '0')
        except ValueError:
            left = 0

        try:
            top = int(self.top or '0')
        except ValueError:
            top = 0

        try:
            right = int(self.right or '0')
        except ValueError:
            right = 0

        try:
            bottom = int(self.bottom or '0')
        except ValueError:
            bottom = 0

        if left < 0:
            left = 0

        if left > self.image.size[0] - 1:
            left = self.image.size[0] - 1

        if top < 0:
            top = 0

        if top > self.image.size[1] - 1:
            top = self.image.size[1] - 1

        if right < 0:
            right = 0

        if right > self.image.size[0] - 1:
            right = self.image.size[0] - 1

        if bottom < 0:
            bottom = 0

        if bottom > self.image.size[1] - 1:
            bottom = self.image.size[1] - 1

        # Invert right value.
        # Pillow uses left, top, right, bottom to define a viewport
        # of real coordinates.
        # We invert the right and bottom to define a viewport
        # that can crop from the right and bottom borders without
        # having to know the real dimensions of an image.
        right = self.image.size[0] - right
        bottom = self.image.size[1] - bottom

        if left > right:
            left = right - 1

        if top > bottom:
            top = bottom - 1

        logger.debug(
            'left: %f, top: %f, right: %f, bottom: %f', left, top, right,
            bottom
        )

        return self.image.crop(box=(left, top, right, bottom))


class TransformationDrawRectangle(
    TransformationDrawRectangleMixin, BaseTransformation
):
    arguments = (
        'left', 'top', 'right', 'bottom', 'fillcolor', 'fill_transparency',
        'outlinecolor', 'outlinewidth'
    )
    label = _('Draw rectangle')
    name = 'draw_rectangle'

    class Form(TransformationDrawRectangleMixin.Form):
        left = forms.IntegerField(
            help_text=_('Left side location in pixels.'), label=_('Left'),
            required=False
        )
        top = forms.IntegerField(
            help_text=_('Top side location in pixels.'), label=_('Top'),
            required=False
        )
        right = forms.IntegerField(
            help_text=_('Right side location in pixels.'), label=_('Right'),
            required=False
        )
        bottom = forms.IntegerField(
            help_text=_('Bottom side location in pixels.'),
            label=_('Bottom'), required=False
        )

    def execute_on(self, *args, **kwargs):
        super().execute_on(*args, **kwargs)

        try:
            left = int(self.left or '0')
        except ValueError:
            left = 0

        try:
            top = int(self.top or '0')
        except ValueError:
            top = 0

        try:
            right = int(self.right or '0')
        except ValueError:
            right = 0

        try:
            bottom = int(self.bottom or '0')
        except ValueError:
            bottom = 0

        if left < 0:
            left = 0

        if left > self.image.size[0] - 1:
            left = self.image.size[0] - 1

        if top < 0:
            top = 0

        if top > self.image.size[1] - 1:
            top = self.image.size[1] - 1

        if right < 0:
            right = 0

        if right > self.image.size[0] - 1:
            right = self.image.size[0] - 1

        if bottom < 0:
            bottom = 0

        if bottom > self.image.size[1] - 1:
            bottom = self.image.size[1] - 1

        # Invert right value.
        # Pillow uses left, top,right, bottom to define a viewport
        # of real coordinates.
        # We invert the right and bottom to define a viewport
        # that can crop from the right and bottom borders without
        # having to know the real dimensions of an image.
        right = self.image.size[0] - right
        bottom = self.image.size[1] - bottom

        if left > right:
            left = right - 1

        if top > bottom:
            top = bottom - 1

        self.bottom = bottom
        self.left = left
        self.top = top
        self.right = right

        return super()._execute_on(self, *args, **kwargs)


class TransformationDrawRectanglePercent(
    TransformationDrawRectangleMixin, BaseTransformation
):
    arguments = (
        'left', 'top', 'right', 'bottom', 'fillcolor', 'fill_transparency',
        'outlinecolor', 'outlinewidth'
    )
    label = _('Draw rectangle (percents coordinates)')
    name = 'draw_rectangle_percent'

    class Form(TransformationDrawRectangleMixin.Form):
        left = forms.FloatField(
            help_text=_('Left side location in percent.'),
            label=_('Left'), required=False
        )
        top = forms.FloatField(
            help_text=_('Top side location in percent.'),
            label=_('Top'), required=False
        )
        right = forms.FloatField(
            help_text=_('Right side location in percent.'),
            label=_('Right'), required=False
        )
        bottom = forms.FloatField(
            help_text=_('Bottom side location in percent.'),
            label=_('Bottom'), required=False
        )

    def execute_on(self, *args, **kwargs):
        super().execute_on(*args, **kwargs)

        try:
            left = float(self.left or '0')
        except ValueError:
            left = 0

        try:
            top = float(self.top or '0')
        except ValueError:
            top = 0

        try:
            right = float(self.right or '0')
        except ValueError:
            right = 0

        try:
            bottom = float(self.bottom or '0')
        except ValueError:
            bottom = 0

        if left < 0:
            left = 0

        if left > 100:
            left = 100

        if top < 0:
            top = 0

        if top > 100:
            top = 100

        if right < 0:
            right = 0

        if right > 100:
            right = 100

        if bottom < 0:
            bottom = 0

        if bottom > 100:
            bottom = 100

        logger.debug(
            'left: %f, top: %f, right: %f, bottom: %f', left, top, right,
            bottom
        )

        left = left / 100.0 * self.image.size[0]
        top = top / 100.0 * self.image.size[1]

        # Invert right value.
        # Pillow uses left, top, right, bottom to define a viewport
        # of real coordinates.
        # We invert the right and bottom to define a viewport
        # that can crop from the right and bottom borders without
        # having to know the real dimensions of an image.

        right = self.image.size[0] - (right / 100.0 * self.image.size[0])
        bottom = self.image.size[1] - (bottom / 100.0 * self.image.size[1])

        self.bottom = bottom
        self.left = left
        self.top = top
        self.right = right

        return super()._execute_on(self, *args, **kwargs)


class TransformationFlip(BaseTransformation):
    arguments = ()
    label = _('Flip')
    name = 'flip'

    def execute_on(self, *args, **kwargs):
        super().execute_on(*args, **kwargs)

        return self.image.transpose(method=Image.FLIP_TOP_BOTTOM)


class TransformationGaussianBlur(BaseTransformation):
    arguments = ('radius',)
    label = _('Gaussian blur')
    name = 'gaussianblur'

    class Form(Form):
        radius = forms.IntegerField(
            initial=2, label=_('Radius'), required=True
        )

    def execute_on(self, *args, **kwargs):
        super().execute_on(*args, **kwargs)

        return self.image.filter(
            filter=ImageFilter.GaussianBlur(radius=self.radius)
        )


class TransformationLineArt(BaseTransformation):
    label = _('Line art')
    name = 'lineart'

    def execute_on(self, *args, **kwargs):
        super().execute_on(*args, **kwargs)

        def lut(x):
            return 0 if x < 128 else 255

        return self.image.convert(mode='L').point(lut=lut, mode='1')


class TransformationMirror(BaseTransformation):
    arguments = ()
    label = _('Mirror')
    name = 'mirror'

    def execute_on(self, *args, **kwargs):
        super().execute_on(*args, **kwargs)

        return self.image.transpose(method=Image.FLIP_LEFT_RIGHT)


class TransformationResize(BaseTransformation):
    arguments = ('width', 'height')
    label = _('Resize')
    name = 'resize'

    class Form(Form):
        width = forms.IntegerField(
            help_text=_(
                'New width in pixels.'
            ), label=_('Width'), required=True
        )
        height = forms.IntegerField(
            help_text=_(
                'New height in pixels.'
            ), label=_('Height'), required=False
        )

    def execute_on(self, *args, **kwargs):
        super().execute_on(*args, **kwargs)

        width = int(self.width)
        height = int(self.height or (1.0 * width / self.aspect))

        factor = 1
        while self.image.size[0] / factor > 2 * width and self.image.size[1] * 2 / factor > 2 * height:
            factor *= 2

        if factor > 1:
            self.image.thumbnail(
                size=(
                    self.image.size[0] / factor,
                    self.image.size[1] / factor
                ), resample=Image.NEAREST
            )

        # Resize the image with best quality algorithm ANTIALIAS.
        self.image.thumbnail(size=(width, height), resample=Image.ANTIALIAS)

        return self.image


class TransformationRotate(BaseTransformation):
    arguments = ('degrees', 'fillcolor')
    label = _('Rotate')
    name = 'rotate'

    class Form(Form):
        degrees = forms.IntegerField(
            help_text=_(
                'Number of degrees to rotate the image counter clockwise '
                'around its center.'
            ), label=_('Degrees'), required=True
        )
        fillcolor = forms.CharField(
            help_text=_(
                'Color to be used for area outside of the rotated image.'
            ), label=_('Fill color'), required=False, widget=ColorWidget()
        )

    def execute_on(self, *args, **kwargs):
        super().execute_on(*args, **kwargs)

        self.degrees = float(self.degrees or '0')
        self.degrees %= 360

        if self.degrees == 0:
            return self.image

        fillcolor_value = getattr(self, 'fillcolor', None)
        if fillcolor_value == 'None':
            fillcolor_value = None

        if fillcolor_value:
            fillcolor = ImageColor.getrgb(color=fillcolor_value)
        else:
            fillcolor = None

        return self.image.rotate(
            angle=360 - self.degrees, resample=Image.BICUBIC, expand=True,
            fillcolor=fillcolor
        )


class TransformationRotate90(TransformationRotate):
    arguments = ()
    degrees = 90
    label = _('Rotate 90 degrees')
    name = 'rotate90'

    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs['degrees'] = 90


class TransformationRotate180(TransformationRotate):
    arguments = ()
    degrees = 180
    label = _('Rotate 180 degrees')
    name = 'rotate180'

    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs['degrees'] = 180


class TransformationRotate270(TransformationRotate):
    arguments = ()
    degrees = 270
    label = _('Rotate 270 degrees')
    name = 'rotate270'

    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs['degrees'] = 270


class TransformationUnsharpMask(BaseTransformation):
    arguments = ('radius', 'percent', 'threshold')
    label = _('Unsharp masking')
    name = 'unsharpmask'

    class Form(Form):
        radius = forms.IntegerField(
            initial=2, help_text=_('The blur radius in pixels.'),
            label=_('Radius'), required=True
        )
        percent = forms.FloatField(
            initial=150, help_text=_('Unsharp strength in percent.'),
            label=_('Percent'), required=True
        )
        threshold = forms.IntegerField(
            initial=3, help_text=_(
                'Minimum brightness change that will be sharpened.'
            ), label=_('Tthreshold'), required=True
        )

    def execute_on(self, *args, **kwargs):
        super().execute_on(*args, **kwargs)

        return self.image.filter(
            ImageFilter.UnsharpMask(
                radius=self.radius, percent=self.percent,
                threshold=self.threshold
            )
        )


class TransformationZoom(BaseTransformation):
    arguments = ('percent',)
    label = _('Zoom')
    name = 'zoom'

    class Form(Form):
        percent = forms.FloatField(
            help_text=_('Zoom level in percent.'),
            label=_('Percent'), required=True
        )

    def execute_on(self, *args, **kwargs):
        super().execute_on(*args, **kwargs)

        percent = float(self.percent or '100')

        if percent == 100:
            return self.image

        decimal_value = percent / 100

        width = int(self.image.size[0] * decimal_value)
        if width < 1:
            width = 1

        height = int(self.image.size[1] * decimal_value)
        if height < 1:
            height = 1

        return self.image.resize(
            size=(width, height), resample=Image.ANTIALIAS
        )


BaseTransformation.register(
    layer=layer_decorations, transformation=TransformationAssetPaste
)
BaseTransformation.register(
    layer=layer_decorations, transformation=TransformationAssetPastePercent
)
BaseTransformation.register(
    layer=layer_decorations, transformation=TransformationAssetWatermark
)
BaseTransformation.register(
    layer=layer_saved_transformations, transformation=TransformationCrop
)
BaseTransformation.register(
    layer=layer_decorations,
    transformation=TransformationDrawRectangle
)
BaseTransformation.register(
    layer=layer_decorations,
    transformation=TransformationDrawRectanglePercent
)
BaseTransformation.register(
    layer=layer_saved_transformations, transformation=TransformationFlip
)
BaseTransformation.register(
    layer=layer_saved_transformations,
    transformation=TransformationGaussianBlur
)
BaseTransformation.register(
    layer=layer_saved_transformations, transformation=TransformationLineArt
)
BaseTransformation.register(
    layer=layer_saved_transformations, transformation=TransformationMirror
)
BaseTransformation.register(
    layer=layer_saved_transformations, transformation=TransformationResize
)
BaseTransformation.register(
    layer=layer_saved_transformations, transformation=TransformationRotate
)
BaseTransformation.register(
    layer=layer_saved_transformations, transformation=TransformationRotate90
)
BaseTransformation.register(
    layer=layer_saved_transformations, transformation=TransformationRotate180
)
BaseTransformation.register(
    layer=layer_saved_transformations, transformation=TransformationRotate270
)
BaseTransformation.register(
    layer=layer_saved_transformations,
    transformation=TransformationUnsharpMask
)
BaseTransformation.register(
    layer=layer_saved_transformations, transformation=TransformationZoom
)
