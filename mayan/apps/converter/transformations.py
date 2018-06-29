from __future__ import unicode_literals

import logging

from PIL import Image, ImageFilter

from django.utils.six import text_type
from django.utils.translation import string_concat, ugettext_lazy as _

logger = logging.getLogger(__name__)


class BaseTransformation(object):
    """
    Transformation can modify the appearance of the document's page preview.
    Some transformation available are: Rotate, zoom, resize and crop.
    """
    arguments = ()
    name = 'base_transformation'
    _registry = {}

    @staticmethod
    def encode_hash(decoded_value):
        return hex(abs(decoded_value))[2:]

    @staticmethod
    def decode_hash(encoded_value):
        return int(encoded_value, 16)

    @staticmethod
    def combine(transformations):
        result = None

        for index, transformation in enumerate(transformations):
            if not result:
                result = hash((BaseTransformation.decode_hash(transformation.cache_hash()), index))
            else:
                result ^= hash((BaseTransformation.decode_hash(transformation.cache_hash()), index))

        return BaseTransformation.encode_hash(result)

    @classmethod
    def register(cls, transformation):
        cls._registry[transformation.name] = transformation

    @classmethod
    def get_transformation_choices(cls):
        return sorted(
            [
                (name, klass.get_label()) for name, klass in cls._registry.items()
            ]
        )

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def get_label(cls):
        if cls.arguments:
            return string_concat(cls.label, ': ', ', '.join(cls.arguments))
        else:
            return cls.label

    def __init__(self, **kwargs):
        self.kwargs = {}
        for argument_name in self.arguments:
            setattr(self, argument_name, kwargs.get(argument_name))
            self.kwargs[argument_name] = kwargs.get(argument_name)

    def cache_hash(self):
        result = text_type.__hash__(self.name)
        for index, (key, value) in enumerate(self.kwargs.items()):
            result ^= hash((key, index)) ^ hash((value, index))

        return BaseTransformation.encode_hash(result)

    def execute_on(self, image):
        self.image = image
        self.aspect = 1.0 * image.size[0] / image.size[1]


class TransformationCrop(BaseTransformation):
    arguments = ('left', 'top', 'right', 'bottom',)
    label = _('Crop')
    name = 'crop'

    def execute_on(self, *args, **kwargs):
        super(TransformationCrop, self).execute_on(*args, **kwargs)

        return self.image.crop(
            (self.left, self.top, self.right, self.bottom)
        )


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
    arguments = ('degrees',)
    label = _('Rotate')
    name = 'rotate'

    def execute_on(self, *args, **kwargs):
        super(TransformationRotate, self).execute_on(*args, **kwargs)

        self.degrees %= 360

        if self.degrees == 0:
            return self.image

        return self.image.rotate(
            360 - self.degrees, resample=Image.BICUBIC, expand=True
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


BaseTransformation.register(TransformationCrop)
BaseTransformation.register(TransformationFlip)
BaseTransformation.register(TransformationGaussianBlur)
BaseTransformation.register(TransformationLineArt)
BaseTransformation.register(TransformationMirror)
BaseTransformation.register(TransformationResize)
BaseTransformation.register(TransformationRotate)
BaseTransformation.register(TransformationRotate90)
BaseTransformation.register(TransformationRotate180)
BaseTransformation.register(TransformationRotate270)
BaseTransformation.register(TransformationUnsharpMask)
BaseTransformation.register(TransformationZoom)
