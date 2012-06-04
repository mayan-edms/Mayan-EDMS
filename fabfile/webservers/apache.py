import os

from fabric.api import run, sudo, cd, env, task, settings
from fabric.contrib.files import upload_template

from ..literals import OS_UBUNTU, OS_FEDORA, OS_DEBIAN


def install_site():
    """
    Install Mayan EDMS's site file in Apache configuration
    """
    #  TODO: configurable site name
    if env.os in [OS_UBUNTU, OS_DEBIAN]:
        upload_template(filename=os.path.join('fabfile', 'templates', 'apache_site'), destination='/etc/apache2/sites-available/mayan', context=env, use_sudo=True)
        sudo('a2ensite mayan') 
    elif env.os == OS_FEDORA:
        upload_template(filename=os.path.join('fabfile', 'templates', 'apache_site'), destination='/etc/httpd/conf.d/mayan.conf', context=env, use_sudo=True)


def remove_site():
    """
    Install Mayan EDMS's site file from Apache's configuration
    """
    if env.os in [OS_UBUNTU, OS_DEBIAN]:
        with settings(warn_only=True):
            sudo('a2dissite mayan')
    elif env.os == OS_FEDORA:
        with settings(warn_only=True):
            sudo('rm /etc/httpd/conf.d/mayan.conf')


def restart():
    """
    Restart Apache
    """
    if env.os in [OS_UBUNTU, OS_DEBIAN]:
        sudo('/etc/init.d/apache2 restart')
    elif env.os == OS_FEDORA:
        sudo('systemctl restart httpd.service')


def reload():
    """
    Reload Apache configuration files
    """
    if env.os in [OS_UBUNTU, OS_DEBIAN]:
        sudo('/etc/init.d/apache2 reload')
    elif env.os == OS_FEDORA:
        sudo('systemctl reload httpd.service')
