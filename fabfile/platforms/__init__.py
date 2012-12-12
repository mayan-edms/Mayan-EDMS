from fabric.api import run, sudo, cd, env, task
from fabric.colors import green

from ..literals import OS_UBUNTU, OS_FEDORA, OS_DEBIAN
from ..conf import setup_environment
import linux, ubuntu, fedora, debian


@task
def install_dependencies():
    """
    Install OS dependencies
    """
    setup_environment()
    print(green('Installing dependencies for %s' % env.os_name, bold=True))
    
    if env.os in [OS_UBUNTU, OS_DEBIAN]:
        debian.install_dependencies()
    elif env.os == OS_FEDORA:
        fedora.install_dependencies()


@task
def install_mayan():
    """
    Install Mayan EDMS
    """
    setup_environment()
    print(green('Installing Mayan EDMS from git repository', bold=True))

    if env.os in [OS_UBUNTU, OS_FEDORA, OS_DEBIAN]:
        linux.install_mayan()


@task
def install_database_manager():
    """
    Install the selected database manager
    """
    setup_environment()
    print(green('Installing database manager: %s' % env.database_manager_name, bold=True))
    
    if env.os in [OS_UBUNTU, OS_DEBIAN]:
        debian.install_database_manager()
    elif env.os == OS_FEDORA:
        fedora.install_database_manager()


@task
def fix_permissions():
    """
    Fix installation files' permissions
    """
    setup_environment()
    print(green('Fixing installation files\' permissions', bold=True))

    if env.os in [OS_UBUNTU, OS_DEBIAN]:
        debian.fix_permissions()
    elif env.os == OS_FEDORA:
        fedora.fix_permissions()


@task
def install_webserver():
    """
    Installing the OS packages for the webserver
    """
    setup_environment()
    print(green('Installing webserver: %s' % env.webserver_name, bold=True))
    
    if env.os in [OS_UBUNTU, OS_DEBIAN]:
        debian.install_webserver()
    elif env.os == OS_FEDORA:
        fedora.install_webserver()

        
@task
def delete_mayan():
    """
    Delete Mayan EDMS from the OS
    """
    setup_environment()
    print(green('Deleting Mayan EDMS files', bold=True))

    if env.os in [OS_UBUNTU, OS_FEDORA, OS_DEBIAN]:
        linux.delete_mayan()
        

@task
def post_install():
    """
    Perform post install operations
    """            
    setup_environment()
    if env.os == OS_UBUNTU:
        ubuntu.post_install()
        linux.post_install()
    elif env.os == OS_FEDORA:
        fedora.post_install()
        linux.post_install()
    elif env.os == OS_DEBIAN:
        debian.post_install()
        linux.post_install()
