from __future__ import absolute_import

import os

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import PIL

from django.utils.safestring import mark_safe
from django.conf import settings

from .literals import (ERROR, SIZE_SMALL, SIZE_BIG, ICONSETS_STATIC_DIRECTORY)


class Icon(object):
    _registry = {}
    _cache = {}

    def __init__(self, id, icon_set=None):
        self.id = id
        self.icon_set = icon_set
        self.__class__._registry[id] = self

    def get_iconset(self):
        from .settings import ICON_SET
        return IconSetBase.get_by_name(self.icon_set or ICON_SET)

    #def get_url(self, size):
    #    #from .settings import ICON_SET
    #    #return IconSetBase.get_by_name(self.icon_set or ICON_SET).get_url_of_icon(self, size)
    #    return self.get_iconset().get_url_of_icon(self, size)
     
    #def get_as_base64(self, size):
    #    from .settings import ICON_SET
    #    return IconSetBase.get_by_name(self.icon_set or ICON_SET).get_as_base64(self, size)

    #def get_as_filename(self, size):
    #    #from .settings import ICON_SET
    #    #return IconSetBase.get_by_name(self.icon_set or ICON_SET).get_filename_of_icon(self, size)        
    #    return self.get_iconset().get_filename_of_icon(self, size)        

    def display(self, size): # TODO: move to widgets?
        #return mark_safe('<img style="vertical-align: middle;" src="%s" />' % self.get_url(size))
        #return mark_safe('<img style="vertical-align: middle;" src="%s" />' % self.get_as_base64(size))
        #return mark_safe('<img style="vertical-align: middle;" src="%s" />' % self.process(size))
        #return mark_safe('<img style="vertical-align: middle;" src="%s" />' % self.get_iconset().compose(self, size))
        
        # Cache a composed icon result for a specific size
        try:
            result = self.__class__._cache['%d_%s' % (id(self), size)]
        except KeyError:
            result = self.get_iconset().compose(self, size)
            self.__class__._cache['%d_%s' % (id(self), size)] = result
            
        return mark_safe('<img style="vertical-align: middle;" src="%s" />' % result)

    def display_small(self):
        return self.display(SIZE_SMALL)

    def display_big(self):
        return self.display(SIZE_BIG)


class IconSetBase(object):
    _registry = {}
    
    @classmethod
    def get_all(cls):
        return cls._registry.values()
    
    @classmethod
    def get_by_name(cls, name):
        return cls._registry.get(name)

    def __init__(self):
        self.__class__._registry[self.name] = self
    
    #def get_filename_of_icon(self, icon, size):
    #    if settings.DEVELOPMENT:
    #        return os.path.join(settings.PROJECT_ROOT, 'apps', 'icons', 'static', ICONSETS_STATIC_DIRECTORY, self.directory, size, self.dictionary.get(icon.id, ERROR))
    #    else:
    #        return os.path.join(settings.STATIC_ROOT, ICONSETS_STATIC_DIRECTORY, self.directory, size, self.dictionary.get(icon.id, ERROR))

    def get_filename_of_image(self, image_name, size):
        if settings.DEVELOPMENT:
            return os.path.join(settings.PROJECT_ROOT, 'apps', 'icons', 'static', ICONSETS_STATIC_DIRECTORY, self.directory, size, image_name)
        else:
            return os.path.join(settings.STATIC_ROOT, ICONSETS_STATIC_DIRECTORY, self.directory, size, image_name)

    #def get_url_of_icon(self, icon, size):
    #    return '%s%s/%s/%s/%s' % (settings.STATIC_URL, ICONSETS_STATIC_DIRECTORY, self.directory, size, self.dictionary.get(icon.id, ERROR))

    def get_major_minor(self, icon):
        return self.dictionary.get(icon.id, self.dictionary.get(ERROR))

    def compose(self, icon, size):
        try:
            major, minor = self.get_major_minor(icon)
        except ValueError:
            major = self.get_major_minor(icon)
            minor = None

        major_image = PIL.Image.open(self.get_filename_of_image(major, size))
        if minor:
            major_width, major_height = major_image.size
            minor_image = PIL.Image.open(self.get_filename_of_image(minor, size))
            minor_image.thumbnail((major_width / 1.6, major_height / 1.6))#, PIL.Image.ANTIALIAS)
            minor_width, minor_height = minor_image.size
            major_image.paste(minor_image, (major_width - minor_width, major_height - minor_height), minor_image)

        output = StringIO()
        major_image.save(output, 'PNG')
        contents = output.getvalue().encode('base64')
        output.close()     
        return 'data:image/png;base64,%s' % contents


class Verb(object):
    pass


class Load(Verb):
    def __init__(self, filename):
        self.filename = filename
    
    def execute(self):
        return PIL.Image.open(self.filename)


class Resize(Verb):
    def __init__(self, image, size, antialias=False):
        self.image = image
        self.size = size
        self.antialias = antialias

    def execute(self):
        if self.antialias:
            self.image.thumbnail(self.size, PIL.Image.ANTIALIAS)
        else:
            self.image.thumbnail(self.size)


class Rotate(Verb):
    def __init__(self, degrees):
        self.degrees = degrees

    def execute(self):
        pass
