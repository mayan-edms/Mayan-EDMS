from __future__ import print_function, unicode_literals

import base64
import hashlib
import json
import shutil
import tarfile

from furl import furl
from pathlib2 import Path
import requests
from semver import max_satisfying

from django.apps import apps
from django.utils.encoding import force_bytes, force_text
from django.utils.functional import cached_property

from mayan.apps.storage.utils import mkdtemp

from .exceptions import DependenciesException

DEFAULT_REGISTRY_URL = 'http://registry.npmjs.com'
DEFAULT_MODULE_DIRECTORY = 'node_modules'
DEFAULT_PACKAGE_FILENAME = 'package.json'
DEFAULT_LOCK_FILENAME = 'package-lock.json'


class NPMPackage(object):
    def __init__(self, registry, name, version):
        self.registry = registry
        self.name = name
        self.version = version

    def download(self):
        algorithm_function = self.get_algorithm_function()
        tar_file_path = self.get_tar_file_path()

        with requests.get(self.version_metadata['dist']['tarball'], stream=True) as response:
            with tar_file_path.open(mode='wb') as file_object:
                shutil.copyfileobj(response.raw, file_object)

        with tar_file_path.open(mode='rb') as file_object:
            integrity_is_good = algorithm_function(file_object.read())

        if not integrity_is_good:
            tar_file_path.unlink()
            raise DependenciesException(
                'Hash of downloaded package doesn\'t match online version.'
            )

    def extract(self):
        shutil.rmtree(
            path=force_text(
                Path(
                    self.registry.module_directory, self.name
                )
            ), ignore_errors=True
        )

        with tarfile.open(name=force_text(self.get_tar_file_path()), mode='r') as file_object:
            file_object.extractall(
                path=force_text(self.registry.module_directory)
            )

        Path(self.registry.module_directory, 'package').rename(
            target=Path(self.registry.module_directory, self.name)
        )

    def get_algorithm_function(self):
        try:
            integrity = self.version_metadata['dist']['integrity']
        except KeyError:
            algorithm_name = 'sha1'
            integrity_value = self.version_metadata['dist']['shasum']
        else:
            algorithm_name, integrity_value = integrity.split('-', 1)

        algorithms = {
            'sha1': lambda data: hashlib.sha1(data).hexdigest() == integrity_value,
            'sha256': lambda data: base64.b64encode(hashlib.sha256(data).digest()) == integrity_value,
            'sha512': lambda data: base64.b64encode(hashlib.sha512(data).digest()) == integrity_value,
        }

        try:
            algorithm = algorithms[algorithm_name]
        except KeyError:
            raise DependenciesException(
                'Unknown hash algorithm: {}'.format(algorithm_name)
            )
        else:
            return algorithm

    def get_best_version(self):
        return max_satisfying(
            self.versions, force_bytes(self.version), loose=True
        )

    def get_tar_file_path(self):
        return Path(
            self.registry.cache_path, self.get_tar_filename()
        )

    def get_tar_filename(self):
        return furl(
            self.version_metadata['dist']['tarball']
        ).path.segments[-1]

    def install(self, include_dependencies=False):
        print('Installing package: {}{}'.format(self.name, self.version))

        self.download()
        self.extract()

        if include_dependencies:
            for name, version in self.version_metadata.get('dependencies', {}).items():
                package = NPMPackage(
                    registry=self.registry, name=name, version=version
                )
                package.install()

    @cached_property
    def metadata(self):
        response = requests.get(url=self.url)
        return response.json()

    @property
    def url(self):
        f = furl(self.registry.url)
        f.path.segments = f.path.segments + [self.name]
        return f.tostr()

    @property
    def version_metadata(self):
        return self.metadata['versions'][self.get_best_version()]

    @property
    def versions(self):
        return [
            force_bytes(version) for version in self.metadata['versions'].keys()
        ]


class NPMRegistry(object):
    def __init__(self, url=None, cache_path=None, module_directory=None, package_filename=None, lock_filename=None):
        self.url = url or DEFAULT_REGISTRY_URL
        self.cache_path = cache_path or mkdtemp()
        self.module_directory = module_directory or DEFAULT_MODULE_DIRECTORY
        self.package_file = package_filename or DEFAULT_PACKAGE_FILENAME
        self.lock_filename = lock_filename or DEFAULT_LOCK_FILENAME

    def _install_package(self, name, version):
        package = NPMPackage(registry=self, name=name, version=version)
        package.install()

    def _read_package(self):
        with self.package_file.open(mode='rb') as file_object:
            self._package_data = json.loads(s=file_object.read())

    def install(self, package=None):
        if package:
            name, version = package.split('@')
            self._install_package(name=name, version=version)
        else:
            self._read_package()

            for name, version in self._package_data['dependencies'].items():
                self._install_package(name=name, version=version)


class JSDependencyManager(object):
    def install(self, app_name=None):
        if app_name:
            app_config_list = [apps.get_app_config(app_label=app_name)]
        else:
            app_config_list = apps.get_app_configs()

        for app in app_config_list:
            path = Path(app.path, 'static')
            entries = list(path.glob('*/package.json'))
            if entries:
                print('Installing JavaScript packages for app: {}'.format(app.label))

                for entry in entries:
                    npm_client = NPMRegistry(
                        module_directory=entry.parent / 'node_modules',
                        package_filename=entry
                    )
                    npm_client.install()
