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
from django.utils.six import PY3

from mayan.apps.storage.utils import mkdtemp

from .exceptions import DependenciesException
from .literals import (
    DEFAULT_LOCK_FILENAME, DEFAULT_MODULE_DIRECTORY, DEFAULT_PACKAGE_FILENAME,
    DEFAULT_REGISTRY_URL,
)


class HashAlgorithm(object):
    DEFAULT_BLOCK_SIZE = 65535
    _registry = {}
    hash_factory = None

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def register(cls, algorithm_class):
        cls._registry[algorithm_class.name] = algorithm_class

    def __init__(self, file_object, block_size=None):
        self.block_size = block_size or self.DEFAULT_BLOCK_SIZE
        self.file_object = file_object
        self.hash_object = self.hash_factory()

    def calculate(self):
        while (True):
            data = self.file_object.read(self.block_size)
            if not data:
                break

            self.hash_object.update(data)

    def get_digest(self):
        return force_text(self._get_digest())


class SHA1Algorithm(HashAlgorithm):
    hash_factory = hashlib.sha1
    name = 'sha1'

    def _get_digest(self):
        return self.hash_object.hexdigest()


class SHA256Algorithm(HashAlgorithm):
    hash_factory = hashlib.sha256
    name = 'sha256'

    def _get_digest(self):
        return base64.b64encode(
            self.hash_object.digest()
        )


class SHA512Algorithm(SHA256Algorithm):
    hash_factory = hashlib.sha512
    name = 'sha512'


HashAlgorithm.register(algorithm_class=SHA1Algorithm)
HashAlgorithm.register(algorithm_class=SHA256Algorithm)
HashAlgorithm.register(algorithm_class=SHA512Algorithm)


class NPMPackage(object):
    def __init__(self, registry, name, version):
        self.registry = registry
        self.name = name
        self.version = version

    def download(self):
        path_tar_file = self.get_tar_file_path()

        with requests.get(self.version_metadata['dist']['tarball'], stream=True) as response:
            response.raise_for_status()
            with path_tar_file.open(mode='wb') as file_object:
                shutil.copyfileobj(response.raw, file_object)

        with path_tar_file.open(mode='rb') as file_object:
            integrity_is_good = self.verify_package_data(file_object=file_object)

        if not integrity_is_good:
            path_tar_file.unlink()
            raise DependenciesException(
                'Hash of downloaded package doesn\'t match online version.'
            )

    def extract(self):
        path_download = Path(
            self.registry.module_directory, self.name
        )
        shutil.rmtree(path=force_text(path_download), ignore_errors=True)

        path_compressed_file = self.get_tar_file_path()
        with tarfile.open(name=force_text(path_compressed_file), mode='r') as file_object:
            file_object.extractall(
                path=force_text(self.registry.module_directory)
            )

        path_target = Path(self.registry.module_directory, self.name)
        # Scoped packages are nested under a parent directory
        # create it to avoid rename errors.
        path_target.mkdir(parents=True)
        Path(self.registry.module_directory, 'package').rename(
            target=force_text(path_target)
        )

    def get_best_version(self):
        # PY3
        # node-semver does a direct str() comparison which means
        # different things on PY2 and PY3
        # Typecast to str in PY3 which is unicode and
        # bytes in PY2 which is str to fool node-semver
        if PY3:
            versions = self.versions
            version = self.version
        else:
            versions = [force_bytes(version) for version in self.versions]
            version = force_bytes(self.version)

        return max_satisfying(
            versions=versions, range_=version, loose=True
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

    def verify_package_data(self, file_object):
        try:
            integrity = self.version_metadata['dist']['integrity']
        except KeyError:
            algorithm_name = 'sha1'
            integrity_value = self.version_metadata['dist']['shasum']
        else:
            algorithm_name, integrity_value = integrity.split('-', 1)

        try:
            algorithm_class = HashAlgorithm.get(name=algorithm_name)
        except KeyError:
            raise DependenciesException(
                'Unknown hash algorithm: {}'.format(algorithm_name)
            )
        else:
            algorithm_object = algorithm_class(file_object=file_object)
            algorithm_object.calculate()
            return algorithm_object.get_digest() == integrity_value

    @property
    def version_metadata(self):
        return self.metadata['versions'][self.get_best_version()]

    @property
    def versions(self):
        return self.metadata['versions'].keys()


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
