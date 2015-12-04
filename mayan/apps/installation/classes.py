from __future__ import unicode_literals

from collections import namedtuple
from json import dumps

import sh

try:
    pip = sh.Command('pip')
except sh.CommandNotFound:
    PIP = False
else:
    PIP = True


class PIPNotFound(Exception):
    pass


class PropertyNamespace(object):
    _registry = {}

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def get_all(cls):
        return cls._registry.values()

    def __init__(self, name, label):
        self.name = name
        self.label = label
        self.properties = {}
        self.__class__._registry[name] = self

    def __unicode__(self):
        return unicode(self.label)

    def __str__(self):
        return str(self.label)

    def add_property(self, *args, **kwargs):
        prop = Property(*args, **kwargs)
        self.properties[prop.name] = prop

    def get_properties(self):
        return self.properties.values()

    @property
    def id(self):
        return self.name


class Property(object):
    _registry = {}

    @classmethod
    def get_all(cls):
        return cls._registry.values()

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def get_reportable(cls, as_dict=False, as_json=False):
        if as_json:
            return dumps(cls.get_reportable(as_dict=True))

        if not as_dict:
            return [prop for prop in cls.get_all() if prop.report]
        else:
            result = {}
            for prop in cls.get_all():
                if prop.report:
                    result[prop.name] = unicode(prop.value)
            return result

    def __init__(self, name, label, value, report=False):
        self.name = name
        self.label = label
        self.value = value
        self.report = report
        self.__class__._registry[name] = self

    def __unicode__(self):
        return unicode(self.value)

    def __str__(self):
        return str(self.value)


Dependency = namedtuple('Dependency', 'name, version, standard')


class VirtualEnv(object):
    def extract_dependency(self, string):
        string = str(string.strip())

        try:
            package, version = string.split('==')
        except ValueError:
            # item is not installed from package, svn/git maybe
            try:
                version, package = string.split('=')
            except:
                # has no version number
                return Dependency(string, version=None, standard=True)
            else:
                # Get rid of '#egg' and '-e'
                version = version.split('#')[0].split(' ')[1]
                return Dependency(package, version, standard=False)
        else:
            return Dependency(package, version, standard=True)

    def get_packages_info(self, requirements_file=None):
        for item in pip('freeze').splitlines():
            yield self.extract_dependency(item)

    def __init__(self):
        if not PIP:
            raise PIPNotFound

    def get_results(self):
        requirements = {}
        installed_packages = {}

        for item in self.get_packages_info():
            requirements[item.name] = item

        for item in self.get_packages_info():
            installed_packages[item.name] = item

        for name, item in requirements.items():
            try:
                if item.standard:
                    if item.version:
                        if item.version == installed_packages[name].version:
                            status = item.version
                        else:
                            status = installed_packages[name].version
                    else:
                        status = None
                else:
                    # Non standard version number, check SVN or GIT path
                    if item.version == installed_packages['%s-dev' % name.replace('-', '_')].version:
                        status = item.version
                    else:
                        status = installed_packages[
                            '%s-dev' % name.replace('-', '_')
                        ].version
            except KeyError:
                # Not installed package found matching with name matching
                # requirement
                status = False

            yield name, item.version, status
