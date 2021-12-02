import hashlib
import logging

from PIL import Image, ImageColor, ImageDraw, ImageFilter

from django.apps import apps
from django.utils.encoding import force_bytes, force_text
from django.utils.text import format_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.http import URL

from .layers import layer_decorations, layer_saved_transformations

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
            result.update(transformation.cache_hash())

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

            result = {}
            for layer, transformations in cls._layer_transformations.items():
                for transformation in transformations:
                    if transformation in flat_transformation_list:
                        result.setdefault(layer, [])
                        result[layer].append(
                            (transformation.name, transformation.get_label())
                        )

            result = [
                (layer.label, transformations) for layer, transformations in result.items()
            ]

            # Sort by transformation group, then each transformation in the
            # group.
            return sorted(result, key=lambda x: (x[0], x[1]))
        else:
            return sorted(
                [
                    (name, klass.get_label()) for name, klass in transformation_list
                ]
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


class AssetTransformationMixin:
    @classmethod
    def get_arguments(cls):
        arguments = super().get_arguments() + (
            'asset_name', 'rotation', 'transparency', 'zoom'
        )
        return arguments

    def _update_hash(self):
        result = super()._update_hash()
        asset = self.get_asset()
        result = hashlib.sha256(force_bytes(s=asset.get_hash()))
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
            lambda i: i * transparency / 100.0
        )

        return {
            'image_asset': image_asset, 'paste_mask': paste_mask
        }


class TransformationAssetPaste(AssetTransformationMixin, BaseTransformation):
    arguments = ('left', 'top')
    label = _('Paste an asset')
    name = 'paste_asset'

    def _execute_on(self, *args, **kwargs):
        try:
            left = int(self.left or '0')
        except ValueError:
            left = 0

        try:
            top = int(self.top or '0')
        except ValueError:
            top = 0

        asset_name = getattr(self, 'asset_name', None)

        if asset_name:
            align_horizontal = getattr(self, 'align_horizontal', 'left')
            align_vertical = getattr(self, 'align_vertical', 'top')

            result = self.get_asset_images()
            if result:
                if align_horizontal == 'left':
                    left = left
                elif align_horizontal == 'center':
                    left = int(left - result['image_asset'].size[0] / 2)
                elif align_horizontal == 'right':
                    left = int(left - result['image_asset'].size[0])

                if align_vertical == 'top':
                    top = top
                elif align_vertical == 'middle':
                    top = int(top - result['image_asset'].size[1] / 2)
                elif align_vertical == 'bottom':
                    top = int(top - result['image_asset'].size[1])

                self.image.paste(
                    im=result['image_asset'], box=(left, top),
                    mask=result['paste_mask']
                )
        else:
            logger.error('No asset name specified.')

        return self.image

    def execute_on(self, *args, **kwargs):
        super().execute_on(*args, **kwargs)
        return self._execute_on(self, *args, **kwargs)


class TransformationAssetPastePercent(TransformationAssetPaste):
    label = _('Paste an asset (percents coordinates)')
    name = 'paste_asset_percent'

    def _execute_on(self, *args, **kwargs):
        try:
            left = float(self.left or '0')
        except ValueError:
            left = 0

        try:
            top = float(self.top or '0')
        except ValueError:
            top = 0

        if left < 0:
            left = 0

        if left > 100:
            left = 100

        if top < 0:
            top = 0

        if top > 100:
            top = 100

        result = self.get_asset_images()

        self.left = left / 100.0 * (
            self.image.size[0] - result['image_asset'].size[0]
        )
        self.top = top / 100.0 * (
            self.image.size[1] - result['image_asset'].size[1]
        )
        self.align_horizontal = 'left'
        self.align_vertical = 'top'

        return super()._execute_on(self, *args, **kwargs)


class TransformationAssetWatermark(
    AssetTransformationMixin, BaseTransformation
):
    arguments = (
        'left', 'top', 'right', 'bottom', 'horizontal_increment',
        'vertical_increment'
    )
    label = _('Paste an asset as watermark')
    name = 'paste_asset_watermark'

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

        asset_name = getattr(self, 'asset_name', None)

        if asset_name:
            result = self.get_asset_images()
            if result:
                try:
                    horizontal_increment = int(self.horizontal_increment or '0')
                except ValueError:
                    horizontal_increment = 0

                try:
                    vertical_increment = int(self.vertical_increment or '0')
                except ValueError:
                    vertical_increment = 0

                if horizontal_increment == 0:
                    horizontal_increment = result['paste_mask'].size[0]

                if vertical_increment == 0:
                    vertical_increment = result['paste_mask'].size[1]

                for x in range(left, right or self.image.size[0], horizontal_increment):
                    for y in range(top, bottom or self.image.size[1], vertical_increment):
                        self.image.paste(
                            im=result['image_asset'], box=(x, y),
                            mask=result['paste_mask']
                        )
        else:
            logger.error('No asset name specified.')

        return self.image


class TransformationCrop(BaseTransformation):
    arguments = ('left', 'top', 'right', 'bottom',)
    label = _('Crop')
    name = 'crop'

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


class TransformationDrawRectangle(BaseTransformation):
    arguments = (
        'left', 'top', 'right', 'bottom', 'fillcolor', 'outlinecolor',
        'outlinewidth'
    )
    label = _('Draw rectangle')
    name = 'draw_rectangle'

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

        logger.debug(
            'left: %f, top: %f, right: %f, bottom: %f', left, top, right,
            bottom
        )

        fillcolor_value = getattr(self, 'fillcolor', None)
        if fillcolor_value:
            fill_color = ImageColor.getrgb(color=fillcolor_value)
        else:
            fill_color = 0

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

        draw = ImageDraw.Draw(image=self.image)
        draw.rectangle(
            xy=(left, top, right, bottom), fill=fill_color,
            outline=outline_color, width=outline_width
        )

        return self.image


class TransformationDrawRectanglePercent(BaseTransformation):
    arguments = (
        'left', 'top', 'right', 'bottom', 'fillcolor', 'outlinecolor',
        'outlinewidth'
    )
    label = _('Draw rectangle (percents coordinates)')
    name = 'draw_rectangle_percent'

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

        fillcolor_value = getattr(self, 'fillcolor', None)
        if fillcolor_value:
            fill_color = ImageColor.getrgb(color=fillcolor_value)
        else:
            fill_color = 0

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

        draw = ImageDraw.Draw(im=self.image)
        draw.rectangle(
            xy=(left, top, right, bottom), fill=fill_color, outline=outline_color,
            width=outline_width
        )

        return self.image


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

    def execute_on(self, *args, **kwargs):
        super().execute_on(*args, **kwargs)

        width = int(self.width)
        height = int(self.height or (1.0 * width / self.aspect))

        factor = 1
        while self.image.size[0] / factor > 2 * width and self.image.size[1] * 2 / factor > 2 * height:
            factor *= 2

        if factor > 1:
            self.image.thumbnail(
                size=(self.image.size[0] / factor, self.image.size[1] / factor),
                resample=Image.NEAREST
            )

        # Resize the image with best quality algorithm ANTIALIAS.
        self.image.thumbnail(size=(width, height), resample=Image.ANTIALIAS)

        return self.image


class TransformationRotate(BaseTransformation):
    arguments = ('degrees', 'fillcolor')
    label = _('Rotate')
    name = 'rotate'

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

    def execute_on(self, *args, **kwargs):
        super().execute_on(*args, **kwargs)

        percent = float(self.percent or '100')

        if percent == 100:
            return self.image

        decimal_value = percent / 100
        return self.image.resize(
            size=(
                int(self.image.size[0] * decimal_value),
                int(self.image.size[1] * decimal_value)
            ), resample=Image.ANTIALIAS
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
    layer=layer_saved_transformations,
    transformation=TransformationDrawRectangle
)
BaseTransformation.register(
    layer=layer_saved_transformations,
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
