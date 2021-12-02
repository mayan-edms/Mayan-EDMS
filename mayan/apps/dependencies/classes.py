import json
from io import BytesIO
import logging
from packaging import version
from pathlib import Path
import pkg_resources
import shutil
import sys
import tarfile

from furl import furl
import requests
from semver import max_satisfying

from django.apps import apps
from django.utils.encoding import force_text
from django.utils.functional import cached_property
from django.utils.module_loading import import_string
from django.utils.termcolors import colorize
from django.utils.translation import ugettext_lazy as _, ugettext

from mayan.apps.common.class_mixins import AppsModuleLoaderMixin
from mayan.apps.common.exceptions import ResolverPipelineError
from mayan.apps.common.utils import ResolverPipelineObjectAttribute
from mayan.apps.storage.utils import (
    TemporaryDirectory, mkdtemp, patch_files as storage_patch_files
)

from .algorithms import HashAlgorithm
from .environments import environment_production
from .exceptions import DependenciesException

logger = logging.getLogger(name=__name__)


class Provider:
    """Base provider class"""


class PyPIRespository(Provider):
    url = 'https://pypi.org/'


class GoogleFontsProvider(Provider):
    url = 'https://fonts.googleapis.com/'


class NPMRegistryRespository(Provider):
    url = 'http://registry.npmjs.com'


class OperatingSystemProvider(Provider):
    """Placeholder for the OS provider"""


class DependencyGroup:
    _registry = {}

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def get_all(cls):
        return sorted(cls._registry.values(), key=lambda x: x.label)

    def __init__(
        self, attribute_name, label, name, allow_multiple=False,
        help_text=None
    ):
        self.allow_multiple = allow_multiple
        self.attribute_name = attribute_name
        self.label = label
        self.help_text = help_text
        self.name = name

        self.__class__._registry[name] = self

    def __str__(self):
        return force_text(s=self.label)

    @staticmethod
    def get_options_for_dependency_group(dependency_group):
        result = []

        for dependency in Dependency.get_all():
            value = ResolverPipelineObjectAttribute.resolve(
                attribute=dependency_group.attribute_name, obj=dependency
            )

            try:
                label = ResolverPipelineObjectAttribute.resolve(
                    attribute='{}_verbose_name'.format(
                        dependency_group.attribute_name
                    ), obj=dependency
                )
            except ResolverPipelineError:
                label = value

            try:
                help_text = ResolverPipelineObjectAttribute.resolve(
                    attribute='{}_help_text'.format(
                        dependency_group.attribute_name
                    ), obj=dependency
                )
            except ResolverPipelineError:
                if dependency_group.allow_multiple:
                    help_text = (None,) * len(value)
                else:
                    help_text = None

            if dependency_group.allow_multiple:
                for entry_index, entry in enumerate(value):
                    dictionary = {
                        'label': label[entry_index], 'help_text': help_text[entry_index], 'value': entry
                    }
                    if dictionary not in result:
                        result.append(dictionary)
            else:
                dictionary = {
                    'label': label, 'help_text': help_text, 'value': value
                }
                if dictionary not in result:
                    result.append(dictionary)

        return result

    def get_entries(self):
        options = DependencyGroup.get_options_for_dependency_group(
            dependency_group=self
        )
        result = []

        for option in options:
            result.append(
                DependencyGroupEntry(
                    dependency_group=self, help_text=option['help_text'],
                    label=option['label'], name=option['value']
                )
            )

        return sorted(result, key=lambda x: x.label)

    def get_entry(self, entry_name):
        for entry in self.get_entries():
            if entry.name == entry_name:
                return entry

        raise KeyError('Entry not found.')


class DependencyGroupEntry:
    def __init__(
        self, dependency_group, label, name, help_text=None
    ):
        self.dependency_group = dependency_group
        self.help_text = help_text or ''
        self.label = label
        self.name = name

    def __str__(self):
        return force_text(s=self.label)

    def get_dependencies(self):
        dependencies = Dependency.get_for_attribute(
            attribute_name=self.dependency_group.attribute_name,
            attribute_value=self.name
        )

        return Dependency.return_sorted(dependencies=dependencies)


class Dependency(AppsModuleLoaderMixin):
    _loader_module_name = 'dependencies'
    _registry = {}

    @staticmethod
    def return_sorted(dependencies):
        return sorted(dependencies, key=lambda x: x.get_label())

    @classmethod
    def _check_all(cls):
        result = []

        for dependency in cls.get_all():
            check = dependency.check()

            if check and any(map(lambda x: x.mark_missing, dependency.environments)):
                check_text = '* {} *'.format(check)
                check_color = check if check else colorize(
                    text=check_text, fg='red', opts=(
                        'bold', 'blink', 'reverse'
                    )
                )

                result.append(
                    {
                        'check': check,
                        'check_text': check_text,
                        'check_color': check_color,
                        'dependency': dependency
                    }
                )

        return result

    @classmethod
    def check_all(cls, as_csv=False, use_color=False):
        if as_csv:
            template = '{},{},{},{},{},{},{}'

            print(
                template.format(
                    ugettext('Name'), ugettext('Type'), ugettext('Version'),
                    ugettext('App'), ugettext('Environments'),
                    ugettext('Other data'), ugettext('Check')
                )
            )
            for result in cls._check_all():
                dependency = result['dependency']

                print(
                    template.format(
                        dependency.name,
                        force_text(s=dependency.class_name_verbose_name),
                        force_text(s=dependency.get_version_string()),
                        force_text(s=dependency.app_label_verbose_name()),
                        force_text(s=dependency.get_environments_verbose_name()),
                        force_text(s=dependency.get_other_data()),
                        force_text(s=result['check'])
                    )
                )
        else:
            for result in cls._check_all():
                dependency = result['dependency']
                print('-' * 40)
                print('* {}'.format(dependency.name))
                print(
                    'Class: {class_name} | Version: {version} '
                    '| App: {app_label} | Environments: {environments} '
                    '| Other data: {other} | Check: {check}'.format(
                        class_name=dependency.class_name_verbose_name,
                        version=dependency.get_version_string(),
                        app_label=dependency.app_label_verbose_name(),
                        environments=dependency.get_environments_verbose_name(),
                        other=dependency.get_other_data(),
                        check=result['check_color'] if use_color else result['check_text']
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
            resolved_attibute_value = ResolverPipelineObjectAttribute.resolve(
                attribute=attribute_name, obj=dependency
            )

            if attribute_value == resolved_attibute_value or attribute_value in resolved_attibute_value:
                result.append(dependency)

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
        self, name, environment=environment_production, app_label=None, copyright_text=None,
        environments=None, help_text=None, label=None, module=None, replace_list=None,
        version_string=None
    ):
        self._app_label = app_label
        self.copyright_text = copyright_text
        self.environments = environments or (environment,)
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

    def get_environments(self):
        return [
            environment.name for environment in self.environments
        ]

    def get_environments_help_text(self):
        return [
            environment.help_text for environment in self.environments
        ]

    def get_environments_verbose_name(self):
        return [
            environment.label for environment in self.environments
        ]

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
        super().__init__(*args, **kwargs)

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
        return super().__init__(*args, **kwargs)

    def _check(self):
        try:
            package_info = self._read_package_file()
        except FileNotFoundError:
            return False

        versions = [package_info['version']]
        version_string = self.version_string

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
        with TemporaryDirectory() as temporary_directory:
            path_compressed_file = self.get_tar_file_path()

            with tarfile.open(name=force_text(s=path_compressed_file), mode='r') as file_object:
                file_object.extractall(path=temporary_directory)

            self.patch_files(path=temporary_directory, replace_list=replace_list)

            path_install = self.get_install_path()

            # Clear the installation path of previous content
            shutil.rmtree(path=force_text(s=path_install), ignore_errors=True)

            # Scoped packages are nested under a parent directory
            # create it to avoid rename errors.
            path_install.mkdir(parents=True)

            # Copy the content under the dependency's extracted content folder
            # 'package' to the final location.
            # We do a copy and delete instead of move because os.rename doesn't
            # support renames across filesystems.
            path_uncompressed_package = Path(temporary_directory, 'package')
            shutil.rmtree(path=force_text(s=path_install))
            shutil.copytree(
                src=force_text(s=path_uncompressed_package),
                dst=force_text(s=path_install)
            )

            # Clean up temporary directory used for download
            shutil.rmtree(path=self.path_cache, ignore_errors=True)

    def download(self):
        self.path_cache = mkdtemp()

        with requests.get(self.version_metadata['dist']['tarball'], stream=True) as response:
            response.raise_for_status()
            with self.get_tar_file_path().open(mode='wb') as file_object:
                shutil.copyfileobj(fsrc=response.raw, fdst=file_object)

    def get_best_version(self):
        versions = self.versions
        version_string = self.version_string

        return max_satisfying(
            versions=versions, range_=version_string, loose=True
        )

    def get_copyright(self):
        path_install_path = self.get_install_path()

        for entry in path_install_path.glob(pattern='LICENSE*'):
            with entry.open(mode='rb') as file_object:
                return force_text(s=file_object.read())

        copyright_text = []

        try:
            package_info = self._read_package_file()
        except FileNotFoundError:
            return super().get_copyright()
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
        except FileNotFoundError:
            return super().get_help_text()
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


class PythonVersion:
    def __init__(self, string):
        self.version = version.parse(string)

    def __lt__(self, other):
        return self.version < other.version


class PythonDependency(Dependency):
    class_name = 'python'
    class_name_help_text = _(
        'Python packages downloaded from PyPI.'
    )
    class_name_verbose_name = _('Python')
    provider_class = PyPIRespository

    def __init__(self, *args, **kwargs):
        self.copyright_attribute = kwargs.pop('copyright_attribute', None)
        super().__init__(*args, **kwargs)

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
            return super().get_copyright()

    def get_latest_version(self):
        url = 'https://pypi.python.org/pypi/{}/json'.format(self.name)
        response = requests.get(url=url)
        versions = list(response.json()['releases'])
        versions.sort(key=PythonVersion)
        return versions[-1]

    def is_latest_version(self):
        return self.version_string == '=={}'.format(self.get_latest_version())


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
        super().__init__(*args, **kwargs)

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
                    s=requests.get(
                        self.url, headers={
                            'User-Agent': agent_string
                        }
                    ).content
                )

                for line in import_file.split('\n'):
                    if 'url' in line:
                        font_url = line.split(' ')[-2][4:-1]
                        url = furl(force_text(s=font_url))
                        font_filename = url.path.segments[-1]

                        path_font_filename = self.path_cache / font_filename
                        with path_font_filename.open(mode='wb') as font_file_object:
                            with requests.get(font_url, stream=True) as response:
                                # Use response.content instead of response.raw
                                # to allow requests to handle gzip and deflate
                                # content.
                                # https://2.python-requests.org/en/master/user/quickstart/#binary-response-content
                                shutil.copyfileobj(
                                    fsrc=BytesIO(response.content),
                                    fdst=font_file_object
                                )

                        line = line.replace(font_url, font_filename)

                    file_object.write(line)

    def extract(self, replace_list=None):
        path_install = self.get_install_path()

        # Clear the installation path of previous content
        shutil.rmtree(path=force_text(s=path_install), ignore_errors=True)

        shutil.copytree(
            src=force_text(s=self.path_cache), dst=force_text(s=path_install)
        )
        shutil.rmtree(path=force_text(s=self.path_cache), ignore_errors=True)

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
    allow_multiple=True, attribute_name='get_environments',
    label=_('Environments'), help_text=_(
        'Dependencies required for an environment might not be required for '
        'another. Example environments: Production, Development.'
    ), name='environment'
)
