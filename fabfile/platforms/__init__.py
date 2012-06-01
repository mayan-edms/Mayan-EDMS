from fabric.api import run, sudo, cd, env, task

from ..literals import OS_UBUNTU
import ubuntu


@task
def install_dependencies():
    """
    Install OS dependencies
    """
    
    print('Installing dependencies for %s' % env.os_name)
    
    if env.os == OS_UBUNTU:
        ubuntu.install_dependencies()


@task
def install_mayan():
    """
    Install Mayan EDMS
    """
    
    print('Installing Mayan EDMS from git repository')

    if env.os == OS_UBUNTU:
        ubuntu.install_mayan()
 

@task
def install_database_manager():
    """
    Install the selected database manager
    """
    
    print('Installing database manager: %s' % env.database_manager_name)
    
    if env.os == OS_UBUNTU:
        ubuntu.install_database_manager()


@task
def fix_permissions():
    """
    Fix installation files' permissions
    """

    print('Fixing installation files\' permissions')

    if env.os == OS_UBUNTU:
        ubuntu.fix_permissions()    


@task
def install_webserver():
    """
    Installing the OS packages for the webserver
    """
    
    print('Installing webserver: %s' % env.webserver_name)
    
    if env.os == OS_UBUNTU:
        ubuntu.install_webserver()
