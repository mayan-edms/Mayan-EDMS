import json
from importlib import import_module
import logging
from pathlib import Path
import pkg_resources
import shutil
import sys
import tarfile

from furl import furl
import requests
from semver import max_satisfying

from django.apps import apps
from django.utils.encoding import (
    force_bytes, force_text, python_2_unicode_compatible
)
from django.utils.functional import cached_property
from django.utils.module_loading import import_string
from django.utils.six import PY3
from django.utils.translation import ugettext_lazy as _, ugettext

from mayan.apps.common.compat import FileNotFoundErrorException
from mayan.apps.common.utils import resolve_attribute
from mayan.apps.storage.utils import mkdtemp, patch_files as storage_patch_files

from .algorithms import HashAlgorithm
from .environments import environment_production
from .exceptions import DependenciesException

logger = logging.getLogger(name=__name__)


class Provider(object):
    """Base provider class"""


class PyPIRespository(Provider):
    url = 'https://pypi.org/'


class GoogleFontsProvider(Provider):
    url = 'https://fonts.googleapis.com/'


class NPMRegistryRespository(Provider):
    url = 'http://registry.npmjs.com'


class OperatingSystemProvider(Provider):
    """Placeholder for the OS provider"""


@python_2_unicode_compatible
class DependencyGroup(object):
    _registry = {}

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def get_all(cls):
        return sorted(cls._registry.values(), key=lambda x: x.label)

    def __init__(self, attribute_name, label, name, help_text=None):
        self.attribute_name = attribute_name
        self.label = label
        self.help_text = help_text
        self.name = name

        self.__class__._registry[name] = self

    def __str__(self):
        return force_text(self.label)

    def get_entries(self):
        results = Dependency.get_values_of_attribute(
            attribute_name=self.attribute_name
        )
        result = []

        for entry in results:
            result.append(
                DependencyGroupEntry(
                    dependency_group=self, help_text=entry['help_text'],
                    label=entry['label'], name=entry['value']
                )
            )

        return sorted(result, key=lambda x: x.label)

    def get_entry(self, entry_name):
        for entry in self.get_entries():
            if entry.name == entry_name:
                return entry

        raise KeyError('Entry not found.')


@python_2_unicode_compatible
class DependencyGroupEntry(object):
    def __init__(self, dependency_group, label, name, help_text=None):
        self.dependency_group = dependency_group
        self.help_text = help_text or ''
        self.label = label
        self.name = name

    def __str__(self):
        return force_text(self.label)

    def get_dependencies(self):
        dependencies = Dependency.get_for_attribute(
            attribute_name=self.dependency_group.attribute_name,
            attribute_value=self.name
        )

        return Dependency.return_sorted(dependencies=dependencies)


class Dependency(object):
    _registry = {}

    @staticmethod
    def initialize():
        for app in apps.get_app_configs():
            try:
                import_module('{}.dependencies'.format(app.name))
            except ImportError as exception:
                if force_text(exception) not in ('No module named dependencies', 'No module named \'{}.dependencies\''.format(app.name)):
                    logger.error(
                        'Error importing %s dependencies.py file; %s', app.name,
                        exception
                    )

    @staticmethod
    def return_sorted(dependencies):
        return sorted(dependencies, key=lambda x: x.get_label())

    @classmethod
    def check_all(cls):
        template = '{:<35}{:<11} {:<15} {:<20} {:<15} {:<30} {:<10}'

        print('\n  ', end='')
        print(
            template.format(
                ugettext('Name'), ugettext('Type'), ugettext('Version'),
                ugettext('App'), ugettext('Environment'),
                ugettext('Other data'), ugettext('Check')
            )
        )
        print('-' * 140)

        for dependency in cls.get_all():
            print('* ', end='')
            print(
                template.format(
                    dependency.name,
                    force_text(dependency.class_name_verbose_name),
                    force_text(dependency.get_version_string()),
                    force_text(dependency.app_label_verbose_name()),
                    force_text(dependency.get_environment_verbose_name()),
                    force_text(dependency.get_other_data()),
                    force_text(dependency.check()),
                )
            )
            sys.stdout.flush()

    @classmethod
    def get(cls, pk):
        return cls._registry[pk]

    @classmethod
    def get_all(cls, subclass_only=False):
        dependencies = cls._registry.values()
        if subclass_only:
            dependencies = [dependency for dependency in dependencies if isinstance(dependency, cls)]

        return Dependency.return_sorted(dependencies=dependencies)

    @classmethod
    def get_for_attribute(cls, attribute_name, attribute_value, **kwargs):
        result = []

        for dependency in cls.get_all(**kwargs):
            if resolve_attribute(attribute=attribute_name, obj=dependency) == attribute_value:
                result.append(dependency)

        return result

    @classmethod
    def get_values_of_attribute(cls, attribute_name):
        result = []

        for dependency in cls.get_all():
            value = resolve_attribute(attribute=attribute_name, obj=dependency)

            try:
                label = resolve_attribute(
                    attribute='{}_verbose_name'.format(attribute_name),
                    obj=dependency
                )
            except AttributeError:
                label = value

            try:
                help_text = resolve_attribute(
                    attribute='{}_help_text'.format(attribute_name),
                    obj=dependency
                )
            except AttributeError:
                help_text = None

            dictionary = {'label': label, 'help_text': help_text, 'value': value}
            if dictionary not in result:
                result.append(dictionary)

        return result

    @classmethod
    def install_multiple(cls, app_label=None, force=False, subclass_only=False):
        for dependency in cls.get_all(subclass_only=subclass_only):
            if app_label:
                if app_label == dependency.app_label:
                    dependency.install(force=force)
            else:
                dependency.install(force=force)

    def __init__(
        self, name, app_label=None, copyright_text=None, help_text=None,
        environment=environment_production, label=None, module=None,
        replace_list=None, version_string=None
    ):
        self._app_label = app_label
        self.copyright_text = copyright_text
        self.environment = environment
        self.help_text = help_text
        self.label = label
        self.module = module
        self.name = name
        self.package_metadata = None
        self.replace_list = replace_list
        self.repository = self.provider_class()
        self.version_string = version_string

        if not app_label:
            if not module:
                raise DependenciesException(
                    _('Need to specify at least one: app_label or module.')
                )

        if self.get_pk() in self.__class__._registry:
            raise DependenciesException(
                _('Dependency "%s" already registered.') % self.name
            )

        self.__class__._registry[self.get_pk()] = self

    @cached_property
    def app_label(self):
        if not self._app_label:
            app = apps.get_containing_app_config(object_name=self.module)
            return app.label
        else:
            return self._app_label

    def app_label_verbose_name(self):
        return apps.get_app_config(app_label=self.app_label).verbose_name

    def download(self):
        """
        Download the dependency from a repository
        """
        raise NotImplementedError

    def get_copyright(self):
        return self.copyright_text or ''

    def install(self, force=False):
        print(_('Installing package: %s... ') % self.get_label_full(), end='')
        sys.stdout.flush()

        if not force:
            if self.check():
                print(_('Already installed.'))
            else:
                self._install()
                print(_('Complete.'))
                sys.stdout.flush()
        else:
            if self.replace_list:
                self.patch_files()
                print(_('Complete.'))
                sys.stdout.flush()

            self.patch_files()
            print(_('Complete.'))
            sys.stdout.flush()

    def _install(self):
        raise NotImplementedError

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)

    def check(self):
        """
        Returns the version found or an exception
        """
        if self._check():
            return True
        else:
            return False

    def check_string(self):
        if self._check():
            return 'True'
        else:
            return 'False'

    def check_string_verbose_name(self):
        if self._check():
            return _('Installed and correct version')
        else:
            return _('Missing or incorrect version')

    def _check(self):
        raise NotImplementedError

    def get_help_text(self):
        return self.help_text or ''

    def get_environment(self):
        return self.environment.name

    def get_environment_help_text(self):
        return self.environment.help_text

    def get_environment_verbose_name(self):
        return self.environment.label

    def get_label(self):
        return self.label or self.name

    def get_label_full(self):
        if self.version_string:
            version_string = '({})'.format(self.version_string)
        else:
            version_string = ''

        return '{} {}'.format(self.get_label(), version_string)

    def get_other_data(self):
        return _('None')

    def get_pk(self):
        return self.name

    def get_url(self):
        raise NotImplementedError

    def get_version_string(self):
        return self.version_string or _('Not specified')

    def patch_files(self, path=None, replace_list=None):
        print(_('Patching files... '), end='')

        try:
            sys.stdout.flush()
        except AttributeError:
            pass

        if not path:
            path = self.get_install_path()

        if not replace_list:
            replace_list = self.replace_list

        storage_patch_files(path=path, replace_list=replace_list)

    def verify(self):
        """
        Verify the integrity of the dependency
        """
        raise NotImplementedError


# Depedency subclasses


class BinaryDependency(Dependency):
    class_name = 'binary'
    class_name_help_text = _(
        'Executables that are called directly by the code.'
    )
    class_name_verbose_name = _('Binary')
    provider_class = OperatingSystemProvider

    def __init__(self, *args, **kwargs):
        self.path = kwargs.pop('path')
        super(BinaryDependency, self).__init__(*args, **kwargs)

    def _check(self):
        return Path(self.path).exists()

    def get_other_data(self):
        return 'Path: {}'.format(self.path)


class JavaScriptDependency(Dependency):
    class_name = 'javascript'
    class_name_help_text = _(
        'JavaScript libraries downloaded the from NPM registry and used for '
        'front-end functionality.'
    )
    class_name_verbose_name = _('JavaScript')
    provider_class = NPMRegistryRespository

    def __init__(self, *args, **kwargs):
        self.static_folder = kwargs.pop('static_folder', None)
        return super(JavaScriptDependency, self).__init__(*args, **kwargs)

    def _check(self):
        try:
            package_info = self._read_package_file()
        except FileNotFoundErrorException:
            return False

        if PY3:
            versions = [package_info['version']]
            version_string = self.version_string
        else:
            versions = [force_bytes(package_info['version'])]
            version_string = force_bytes(self.version_string)

        return max_satisfying(
            versions=versions, range_=version_string,
            loose=True
        )

    def _read_package_file(self):
        path_install_path = self.get_install_path()
        path_package = path_install_path / 'package.json'

        with path_package.open(mode='rb') as file_object:
            return json.load(file_object)

    def _install(self, include_dependencies=False):
        self.get_metadata()
        print(_('Downloading... '), end='')
        sys.stdout.flush()
        self.download()
        print(_('Verifying... '), end='')
        sys.stdout.flush()
        self.verify()
        print(_('Extracting... '), end='')
        sys.stdout.flush()
        self.extract()

        if include_dependencies:
            for name, version_string in self.version_metadata.get('dependencies', {}).items():
                dependency = JavaScriptDependency(
                    name=name, version_string=version_string
                )
                dependency.install(include_dependencies=False)

    def extract(self, replace_list=None):
        temporary_directory = mkdtemp()
        path_compressed_file = self.get_tar_file_path()

        with tarfile.open(name=force_text(path_compressed_file), mode='r') as file_object:
            file_object.extractall(path=temporary_directory)

        self.patch_files(path=temporary_directory, replace_list=replace_list)

        path_install = self.get_install_path()

        # Clear the installation path of previous content
        shutil.rmtree(path=force_text(path_install), ignore_errors=True)

        # Scoped packages are nested under a parent directory
        # create it to avoid rename errors.
        path_install.mkdir(parents=True)

        # Copy the content under the dependency's extracted content folder
        # 'package' to the final location.
        # We do a copy and delete instead of move because os.rename doesn't
        # support renames across filesystems.
        path_uncompressed_package = Path(temporary_directory, 'package')
        shutil.rmtree(force_text(path_install))
        shutil.copytree(
            force_text(path_uncompressed_package), force_text(path_install)
        )
        shutil.rmtree(force_text(path_uncompressed_package))

        # Clean up temporary directory used for download
        shutil.rmtree(path=temporary_directory, ignore_errors=True)
        shutil.rmtree(path=self.path_cache, ignore_errors=True)

    def download(self):
        self.path_cache = mkdtemp()

        with requests.get(self.version_metadata['dist']['tarball'], stream=True) as response:
            response.raise_for_status()
            with self.get_tar_file_path().open(mode='wb') as file_object:
                shutil.copyfileobj(fsrc=response.raw, fdst=file_object)

    def get_best_version(self):
        # PY3
        # node-semver does a direct str() comparison which means
        # different things on PY2 and PY3
        # Typecast to str in PY3 which is unicode and
        # bytes in PY2 which is str to fool node-semver
        if PY3:
            versions = self.versions
            version_string = self.version_string
        else:
            versions = [force_bytes(version) for version in self.versions]
            version_string = force_bytes(self.version_string)

        return max_satisfying(
            versions=versions, range_=version_string, loose=True
        )

    def get_copyright(self):
        path_install_path = self.get_install_path()

        for entry in path_install_path.glob(pattern='LICENSE*'):
            with entry.open(mode='rb') as file_object:
                return force_text(file_object.read())

        copyright_text = []

        try:
            package_info = self._read_package_file()
        except FileNotFoundErrorException:
            return super(JavaScriptDependency, self).get_copyright()
        else:
            copyright_text.append(
                package_info.get('license') or package_info.get(
                    'licenses'
                )[0]['type']
            )
            author = package_info.get('author', {})

            try:
                author = author.get('name')
            except AttributeError:
                pass

            copyright_text.append(author or '')
            return '\n'.join(copyright_text)

    def get_help_text(self):
        description = None

        try:
            description = self._read_package_file().get('description')
        except FileNotFoundErrorException:
            return super(JavaScriptDependency, self).get_help_text()
        else:
            return description

    def get_install_path(self):
        app = apps.get_app_config(app_label=self.app_label)
        result = Path(
            app.path, 'static', self.static_folder or app.label,
            'node_modules', self.name
        )
        return result

    def get_metadata(self):
        response = requests.get(url=self.get_url())
        self.package_metadata = response.json()
        self.versions = self.package_metadata['versions'].keys()
        self.version_best = self.get_best_version()
        try:
            self.version_metadata = self.package_metadata['versions'][
                self.version_best
            ]
        except KeyError:
            raise DependenciesException(
                'Best version for dependency %s is not found in '
                'upstream repository.', self.version_best
            )

    def get_tar_file_path(self):
        return Path(
            self.path_cache, self.get_tar_filename()
        )

    def get_tar_filename(self):
        return furl(
            self.version_metadata['dist']['tarball']
        ).path.segments[-1]

    def get_url(self):
        url = furl(self.repository.url)
        url.path.segments = url.path.segments + [self.name]
        return url.tostr()

    def verify(self):
        path_tar_file = self.get_tar_file_path()

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
                'Unknown hash algorithm: %s', algorithm_name
            )

        with path_tar_file.open(mode='rb') as file_object:
            algorithm_object = algorithm_class(file_object=file_object)
            algorithm_object.calculate()

        if algorithm_object.get_digest() != integrity_value:
            path_tar_file.unlink()
            raise DependenciesException(
                'Hash of downloaded dependency package "%s" doesn\'t match '
                'online version.', self.get_label_full()
            )


class PythonDependency(Dependency):
    class_name = 'python'
    class_name_help_text = _(
        'Python packages downloaded from PyPI.'
    )
    class_name_verbose_name = _('Python')
    provider_class = PyPIRespository

    def __init__(self, *args, **kwargs):
        self.copyright_attribute = kwargs.pop('copyright_attribute', None)
        super(PythonDependency, self).__init__(*args, **kwargs)

    def _check(self):
        try:
            return pkg_resources.get_distribution(
                dist='{}{}'.format(self.name, self.version_string)
            ) is not None
        except pkg_resources.DistributionNotFound:
            return False
        except pkg_resources.VersionConflict:
            return False

    def get_copyright(self):
        if self.copyright_attribute:
            return import_string(dotted_path=self.copyright_attribute)
        else:
            return super(PythonDependency, self).get_copyright()


class GoogleFontDependency(Dependency):
    class_name = 'google_font'
    class_name_help_text = _(
        'Fonts downloaded from fonts.googleapis.com.'
    )
    class_name_verbose_name = _('Google font')
    provider_class = GoogleFontsProvider
    user_agents = {
        'woff2': 'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0',
        'woff': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
        'ttf': 'Mozilla/5.0 (Linux; U; Android 2.2; en-us; DROID2 GLOBAL Build/S273) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    }

    def __init__(self, *args, **kwargs):
        self.url = kwargs.pop('url')
        self.static_folder = kwargs.pop('static_folder', None)
        super(GoogleFontDependency, self).__init__(*args, **kwargs)

    def _check(self):
        return self.get_install_path().exists()

    def _install(self):
        print(_('Downloading... '), end='')
        sys.stdout.flush()
        self.download()
        print(_('Extracting... '), end='')
        sys.stdout.flush()
        self.extract()

    def download(self):
        self.path_cache = Path(mkdtemp())
        # Use .css to keep the same ContentType, otherwise the webserver
        # will use the generic octet and the browser will ignore the import
        # https://www.w3.org/TR/2013/CR-css-cascade-3-20131003/#content-type
        self.path_import_file = self.path_cache / 'import.css'

        self.font_files = []

        with self.path_import_file.open(mode='w') as file_object:
            for agent_name, agent_string in self.user_agents.items():
                import_file = force_text(
                    requests.get(
                        self.url, headers={
                            'User-Agent': agent_string
                        }
                    ).content
                )

                for line in import_file.split('\n'):
                    if 'url' in line:
                        font_url = line.split(' ')[-2][4:-1]
                        url = furl(force_text(font_url))
                        font_filename = url.path.segments[-1]

                        path_font_filename = self.path_cache / font_filename
                        with path_font_filename.open(mode='wb') as font_file_object:
                            with requests.get(font_url, stream=True) as response:
                                shutil.copyfileobj(fsrc=response.raw, fdst=font_file_object)

                        line = line.replace(font_url, font_filename)

                    file_object.write(line)

    def extract(self, replace_list=None):
        path_install = self.get_install_path()

        # Clear the installation path of previous content
        shutil.rmtree(path=force_text(path_install), ignore_errors=True)

        shutil.copytree(
            force_text(self.path_cache), force_text(path_install)
        )
        shutil.rmtree(force_text(self.path_cache), ignore_errors=True)

    def get_install_path(self):
        app = apps.get_app_config(app_label=self.app_label)
        result = Path(
            app.path, 'static', self.static_folder or app.label,
            'google_fonts', self.name
        )
        return result


DependencyGroup(
    attribute_name='app_label', label=_('Declared in app'), help_text=_(
        'Show dependencies by the app that declared them.'
    ), name='app'
)
DependencyGroup(
    attribute_name='class_name', label=_('Class'), help_text=_(
        'Show the different classes of dependencies. Classes are usually '
        'divided by language or the file types of the dependency.'
    ), name='class'
)
DependencyGroup(
    attribute_name='check_string', label=_('State'), help_text=_(
        'Show the different states of the dependencies. True means that the '
        'dependencies is installed and is of a correct version. False means '
        'the dependencies is missing or an incorrect version is present.'
    ), name='state'
)
DependencyGroup(
    attribute_name='get_environment', label=_('Environment'), help_text=_(
        'Dependencies required for an environment might not be required for '
        'another. Example environments: Production, Development.'
    ), name='environment'
)
