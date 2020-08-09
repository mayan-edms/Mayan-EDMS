import hashlib
import logging

from PIL import Image, ImageColor, ImageDraw, ImageFilter

from django.apps import apps
from django.utils.encoding import force_bytes, force_text
from django.utils.text import format_lazy
from django.utils.translation import ugettext_lazy as _

from .layers import layer_decorations, layer_saved_transformations

logger = logging.getLogger(name=__name__)


class BaseTransformationType(type):
    def __str__(self):
        return force_text(self.label)


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
        result = None

        for transformation in transformations:
            if not result:
                result = hashlib.sha256(transformation.cache_hash())
            else:
                result.update(transformation.cache_hash())

        return result.hexdigest()

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def get_label(cls):
        if cls.arguments:
            return format_lazy('{}: {}', cls.label, ', '.join(cls.arguments))
        else:
            return cls.label

    @classmethod
    def get_transformation_choices(cls, layer=None):
        if layer:
            transformation_list = [
                (transformation.name, transformation) for transformation in cls._layer_transformations[layer]
            ]
        else:
            transformation_list = cls._registry.items()

        return sorted(
            [
                (name, klass.get_label()) for name, klass in transformation_list
            ]
        )

    @classmethod
    def register(cls, layer, transformation):
        cls._registry[transformation.name] = transformation
        cls._layer_transformations.setdefault(layer, [])
        cls._layer_transformations[layer].append(transformation)

    def __init__(self, **kwargs):
        self.kwargs = {}
        for argument_name in self.arguments:
            setattr(self, argument_name, kwargs.get(argument_name))
            self.kwargs[argument_name] = kwargs.get(argument_name)

    def cache_hash(self):
        result = hashlib.sha256(force_bytes(self.name))

        # Sort arguments for guaranteed repeatability
        for key, value in sorted(self.kwargs.items()):
            result.update(force_bytes(key))
            result.update(force_bytes(value))

        return force_bytes(result.hexdigest())

    def execute_on(self, image):
        self.image = image
        self.aspect = 1.0 * image.size[0] / image.size[1]


class TransformationAssetPaste(BaseTransformation):
    arguments = (
        'left', 'top', 'asset_name', 'rotation', 'transparency', 'zoom'
    )
    label = _('Paste an asset')
    name = 'paste_asset'

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

        asset_name = getattr(self, 'asset_name', None)

        if asset_name:
            Asset = apps.get_model(app_label='converter', model_name='Asset')

            try:
                asset = Asset.objects.get(internal_name=asset_name)
            except Asset.DoesNotExist:
                logger.error('Asset "%s" not found.', asset_name)
                return self.image
            else:
                with asset.open() as file_object:
                    image_asset = Image.open(fp=file_object)

                    if image_asset.mode != 'RGBA':
                        image_asset.putalpha(alpha=255)

                    image_asset = image_asset.rotate(
                        angle=360 - rotation, resample=Image.BICUBIC,
                        expand=True
                    )

                    if zoom != 100.0:
                        decimal_value = zoom / 100.0
                        image_asset = image_asset.resize(
                            (
                                int(image_asset.size[0] * decimal_value),
                                int(image_asset.size[1] * decimal_value)
                            ), Image.ANTIALIAS
                        )

                    paste_mask = image_asset.getchannel(channel='A').point(
                        lambda i: i * transparency / 100.0
                    )

                    self.image.paste(
                        im=image_asset, box=(top, left), mask=paste_mask
                    )
        else:
            logger.error('No asset name specified.')

        return self.image


class TransformationCrop(BaseTransformation):
    arguments = ('left', 'top', 'right', 'bottom',)
    label = _('Crop')
    name = 'crop'

    def execute_on(self, *args, **kwargs):
        super(TransformationCrop, self).execute_on(*args, **kwargs)

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

        # Invert right value
        # Pillow uses left, top, right, bottom to define a viewport
        # of real coordinates
        # We invert the right and bottom to define a viewport
        # that can crop from the right and bottom borders without
        # having to know the real dimensions of an image
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

        return self.image.crop((left, top, right, bottom))


class TransformationDrawRectangle(BaseTransformation):
    arguments = (
        'left', 'top', 'right', 'bottom', 'fillcolor', 'outlinecolor',
        'outlinewidth'
    )
    label = _('Draw rectangle')
    name = 'draw_rectangle'

    def execute_on(self, *args, **kwargs):
        super(TransformationDrawRectangle, self).execute_on(*args, **kwargs)

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

        # Invert right value
        # Pillow uses left, top, right, bottom to define a viewport
        # of real coordinates
        # We invert the right and bottom to define a viewport
        # that can crop from the right and bottom borders without
        # having to know the real dimensions of an image
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
            fill_color = ImageColor.getrgb(fillcolor_value)
        else:
            fill_color = 0

        outlinecolor_value = getattr(self, 'outlinecolor', None)
        if outlinecolor_value:
            outline_color = ImageColor.getrgb(outlinecolor_value)
        else:
            outline_color = None

        outlinewidth_value = getattr(self, 'outlinewidth', None)
        if outlinewidth_value:
            outline_width = int(outlinewidth_value)
        else:
            outline_width = 0

        draw = ImageDraw.Draw(self.image)
        draw.rectangle(
            (left, top, right, bottom), fill=fill_color, outline=outline_color,
            width=outline_width
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
        super(TransformationDrawRectanglePercent, self).execute_on(*args, **kwargs)

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
            fill_color = ImageColor.getrgb(fillcolor_value)
        else:
            fill_color = 0

        outlinecolor_value = getattr(self, 'outlinecolor', None)
        if outlinecolor_value:
            outline_color = ImageColor.getrgb(outlinecolor_value)
        else:
            outline_color = None

        outlinewidth_value = getattr(self, 'outlinewidth', None)
        if outlinewidth_value:
            outline_width = int(outlinewidth_value)
        else:
            outline_width = 0

        left = left / 100.0 * self.image.size[0]
        top = top / 100.0 * self.image.size[1]

        # Invert right value
        # Pillow uses left, top, right, bottom to define a viewport
        # of real coordinates
        # We invert the right and bottom to define a viewport
        # that can crop from the right and bottom borders without
        # having to know the real dimensions of an image

        right = self.image.size[0] - (right / 100.0 * self.image.size[0])
        bottom = self.image.size[1] - (bottom / 100.0 * self.image.size[1])

        draw = ImageDraw.Draw(self.image)
        draw.rectangle(
            (left, top, right, bottom), fill=fill_color, outline=outline_color,
            width=outline_width
        )

        return self.image


class TransformationFlip(BaseTransformation):
    arguments = ()
    label = _('Flip')
    name = 'flip'

    def execute_on(self, *args, **kwargs):
        super(TransformationFlip, self).execute_on(*args, **kwargs)

        return self.image.transpose(Image.FLIP_TOP_BOTTOM)


class TransformationGaussianBlur(BaseTransformation):
    arguments = ('radius',)
    label = _('Gaussian blur')
    name = 'gaussianblur'

    def execute_on(self, *args, **kwargs):
        super(TransformationGaussianBlur, self).execute_on(*args, **kwargs)

        return self.image.filter(ImageFilter.GaussianBlur(radius=self.radius))


class TransformationLineArt(BaseTransformation):
    label = _('Line art')
    name = 'lineart'

    def execute_on(self, *args, **kwargs):
        super(TransformationLineArt, self).execute_on(*args, **kwargs)

        return self.image.convert('L').point(lambda x: 0 if x < 128 else 255, '1')


class TransformationMirror(BaseTransformation):
    arguments = ()
    label = _('Mirror')
    name = 'mirror'

    def execute_on(self, *args, **kwargs):
        super(TransformationMirror, self).execute_on(*args, **kwargs)

        return self.image.transpose(Image.FLIP_LEFT_RIGHT)


class TransformationResize(BaseTransformation):
    arguments = ('width', 'height')
    label = _('Resize')
    name = 'resize'

    def execute_on(self, *args, **kwargs):
        super(TransformationResize, self).execute_on(*args, **kwargs)

        width = int(self.width)
        height = int(self.height or 1.0 * width / self.aspect)

        factor = 1
        while self.image.size[0] / factor > 2 * width and self.image.size[1] * 2 / factor > 2 * height:
            factor *= 2

        if factor > 1:
            self.image.thumbnail(
                (self.image.size[0] / factor, self.image.size[1] / factor),
                Image.NEAREST
            )

        # Resize the image with best quality algorithm ANTI-ALIAS
        self.image.thumbnail((width, height), Image.ANTIALIAS)

        return self.image


class TransformationRotate(BaseTransformation):
    arguments = ('degrees', 'fillcolor')
    label = _('Rotate')
    name = 'rotate'

    def execute_on(self, *args, **kwargs):
        super(TransformationRotate, self).execute_on(*args, **kwargs)

        self.degrees %= 360

        if self.degrees == 0:
            return self.image

        fillcolor_value = getattr(self, 'fillcolor', None)
        if fillcolor_value:
            fillcolor = ImageColor.getrgb(fillcolor_value)
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
        super(TransformationRotate90, self).__init__()
        self.kwargs['degrees'] = 90


class TransformationRotate180(TransformationRotate):
    arguments = ()
    degrees = 180
    label = _('Rotate 180 degrees')
    name = 'rotate180'

    def __init__(self, **kwargs):
        super(TransformationRotate180, self).__init__()
        self.kwargs['degrees'] = 180


class TransformationRotate270(TransformationRotate):
    arguments = ()
    degrees = 270
    label = _('Rotate 270 degrees')
    name = 'rotate270'

    def __init__(self, **kwargs):
        super(TransformationRotate270, self).__init__()
        self.kwargs['degrees'] = 270


class TransformationUnsharpMask(BaseTransformation):
    arguments = ('radius', 'percent', 'threshold')
    label = _('Unsharp masking')
    name = 'unsharpmask'

    def execute_on(self, *args, **kwargs):
        super(TransformationUnsharpMask, self).execute_on(*args, **kwargs)

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
        super(TransformationZoom, self).execute_on(*args, **kwargs)

        if self.percent == 100:
            return self.image

        decimal_value = float(self.percent) / 100
        return self.image.resize(
            (
                int(self.image.size[0] * decimal_value),
                int(self.image.size[1] * decimal_value)
            ), Image.ANTIALIAS
        )


BaseTransformation.register(
    layer=layer_decorations, transformation=TransformationAssetPaste
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

"""


class TransformationWatermark(BaseTransformation):
    arguments = ('box',)
    label = _('Paste an asset as watermark')
    name = 'paste_asset_watermark'

    # x_offset, y_offset, x_increment, y_increment, rotation, alpha

    def execute_on(self, *args, **kwargs):
        super().execute_on(*args, **kwargs)

        box = getattr(self, 'box', None)

        source_image = Image.open('/tmp/test_image.png')
        source_image.putalpha(75)
        source_image = source_image.rotate(
            angle=45, resample=Image.BICUBIC
            #, expand=True,
            #fillcolor=fillcolor
        )


        for i in range(0, self.image.size[0], 500):
            for j in range(0, self.image.size[1], 250):
                self.image.paste(source_image, (i, j), source_image)

        #self.image.paste(im=source_image, box=box, mask=source_image)
        #background.paste(im=source_image, box=box, mask=source_image)
        return self.image
        #return background

        #background = self.image.convert('RGBA')
        #return Image.alpha_composite(background, source_image)



BaseTransformation.register(
    layer=layer_decorations, transformation=TransformationWatermark
)
"""
