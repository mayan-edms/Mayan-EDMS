from __future__ import print_function, unicode_literals

import base64
import hashlib
import json
import os
import shutil
import tarfile

from furl import furl
from pathlib2 import Path
import requests
from semver import max_satisfying

from django.apps import apps
from django.utils.encoding import force_bytes

from .exceptions import NPMException, NPMPackgeIntegrityError
from .utils import mkdtemp


class NPMPackage(object):
    def __init__(self, registry, name, version):
        self.registry = registry
        self.name = name
        self.version = version

    def _download(self):
        with requests.get(self.download_metadata['dist']['tarball'], stream=True) as response:
            with open(name=self.tar_file_path, mode='wb') as file_object:
                file_object.write(response.content)

        try:
            upstream_algorithm_name, upstream_integrity_value = self.download_metadata['dist']['integrity'].split('-', 1)
        except KeyError:
            upstream_algorithm_name = 'sha1'
            upstream_integrity_value = self.download_metadata['dist']['shasum']

        algorithms = {
            'sha1': lambda data: hashlib.sha1(data).hexdigest(),
            'sha256': lambda data: base64.b64encode(hashlib.sha256(data).digest()),
            'sha512': lambda data: base64.b64encode(hashlib.sha512(data).digest()),
        }

        try:
            algorithm = algorithms[upstream_algorithm_name]
        except KeyError:
            raise NPMException(
                'Unknown hash algorithm: {}'.format(upstream_algorithm_name)
            )

        with open(name=self.tar_file_path, mode='rb') as file_object:
            integrity_value = algorithm(file_object.read())

        if integrity_value != upstream_integrity_value:
            os.unlink(self.tar_file_path)
            raise NPMPackgeIntegrityError(
                'Hash of downloaded package doesn\'t match online version.'
            )

    def _extract(self):
        shutil.rmtree(
            os.path.join(
                self.registry.module_directory, self.name
            ), ignore_errors=True
        )

        with tarfile.open(name=self.tar_file_path, mode='r') as file_object:
            file_object.extractall(path=self.registry.module_directory)

        os.rename(
            os.path.join(self.registry.module_directory, 'package'),
            os.path.join(self.registry.module_directory, self.name)
        )

    @property
    def best_version(self):
        if not hasattr(self, '_best_version'):
            self._best_version = max_satisfying(
                self.versions, force_bytes(self.version), loose=True
            )
            print('Best version: {}'.format(self._best_version))

        return self._best_version

    @property
    def download_metadata(self):
        if not hasattr(self, '_download_metadata'):
            response = requests.get(url=self.download_url)
            self._download_metadata = response.json()
        return self._download_metadata

    @property
    def download_url(self):
        f = furl(self.url)
        f.path.segments = f.path.segments + [self.best_version]
        return f.tostr()

    def install(self, include_dependencies=False):
        print('Installing package: {}{}'.format(self.name, self.version))

        self._download()
        self._extract()

        if include_dependencies:
            for name, version in self.download_metadata.get('dependencies', {}).items():
                package = NPMPackage(
                    registry=self.registry, name=name, version=version
                )
                package.install()

    @property
    def tar_filename(self):
        if not hasattr(self, '_tar_filename'):
            self._tar_filename = furl(
                self.download_metadata['dist']['tarball']
            ).path.segments[-1]

        return self._tar_filename

    @property
    def tar_file_path(self):
        if not hasattr(self, '_tar_file_path'):
            self._tar_file_path = os.path.join(
                self.registry.cache_path, self.tar_filename
            )

        return self._tar_file_path

    @property
    def url(self):
        f = furl(self.registry.url)
        f.path.segments = f.path.segments + [self.name]
        return f.tostr()

    @property
    def versions(self):
        if not hasattr(self, '_versions'):
            response = requests.get(url=self.url)
            self._versions = [
                force_bytes(version) for version in response.json()['versions'].keys()
            ]

        return self._versions


class NPMRegistry(object):
    DEFAULT_REGISTRY_URL = 'http://registry.npmjs.com'
    DEFAULT_MODULE_DIRECTORY = 'node_modules'
    DEFAULT_PACKAGE_FILENAME = 'package.json'
    DEFAULT_LOCK_FILENAME = 'package-lock.json'

    def __init__(self, url=None, cache_path=None, module_directory=None, package_filename=None, lock_filename=None):
        self.url = url or self.DEFAULT_REGISTRY_URL
        self.cache_path = cache_path or mkdtemp()
        self.module_directory = module_directory or self.DEFAULT_MODULE_DIRECTORY
        self.package_file = package_filename or self.DEFAULT_PACKAGE_FILENAME
        self.lock_filename = lock_filename or self.DEFAULT_LOCK_FILENAME

    def _install_package(self, name, version):
        package = NPMPackage(registry=self, name=name, version=version)
        package.install()

    def _read_package(self):
        with open(self.package_file) as file_object:
            self._package_data = json.loads(file_object.read())

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
            for root, dirs, files in os.walk(os.path.join(app.path, 'static')):
                if 'package.json' in files and not (set(Path(root).parts) & set(['node_modules', 'packages', 'vendors'])):
                    print('Installing JavaScript packages for app: {} - {}'.format(app.label, root))
                    npm_client = NPMRegistry(
                        module_directory=os.path.join(root, 'node_modules'),
                        package_filename=os.path.join(root, 'package.json')
                    )
                    npm_client.install()
