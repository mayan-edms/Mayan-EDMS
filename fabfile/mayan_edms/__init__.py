from distutils.version import LooseVersion
import importlib

from fabric.api import env, task, cd, sudo, settings
from fabric.colors import green, red

from ..conf import setup_environment


@task
def upgrade():
    """
    Upgrade a Mayan EDMS installation, but doing incremental upgrades
    """
    setup_environment()
    print(green('Upgrading Mayan EDMS database', bold=True))

    with settings(warn_only=True):
        with cd(env.virtualenv_path):
            version = sudo('source bin/activate; python -c "import os;os.environ[\'DJANGO_SETTINGS_MODULE\']=\'mayan.settings\';from django.core.management import setup_environ;import settings;setup_environ(settings);import main;print main.__version__"')

    if version.failed:
        print(red('Unable to determined the current version.', bold=True))
        exit()

    current_verision = 'v%s' % version
    print(green('Current version: %s' % version, bold=True))
    
    with settings(warn_only=True):
        with cd(env.repository_name):
            tags = sudo('git tag').split('\r\n')
    
    if tags.failed:
        print(red('Upgrading is only support on git based installations.', bold=True))
        exit()
    
    tags.sort(key=LooseVersion)

    latest_version = tags[-1]
    print(green('Latest version: %s' % latest_version, bold=True))

    upgrade_steps = tags.index(latest_version) - tags.index(current_verision)
    if not upgrade_steps:
        print(green('Already in the latest version, no need to upgrade.', bold=True))
        exit()
    else:
        print(green('Upgrade steps needed until latest version: %d' % (), bold=True))
        version_module_name = current_verision.replace('.', '_')
        module = importlib.import_module('fabfile.mayan_edms.upgrades.%s' % version_module_name)
        module.upgrade()
