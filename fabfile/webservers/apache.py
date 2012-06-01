import os

from fabric.api import run, sudo, cd, env, task
from fabric.contrib.files import upload_template


def install_site():
    """
    Install Mayan EDMS's site file in Apache configuration
    """
    #  TODO: configurable site name
    upload_template(filename=os.path.join('fabfile', 'templates', 'apache_site'), destination='/etc/apache2/sites-available/mayan', context=env, use_sudo=True)
    sudo('a2ensite mayan') 


def remove_site():
    """
    Install Mayan EDMS's site file from Apache's configuration
    """
    sudo('a2dissite mayan')


def restart():
    """
    Restart Apache
    """
    sudo('/etc/init.d/apache2 restart')


def reload():
    """
    Reload Apache configuration files
    """
    sudo('/etc/init.d/apache2 reload')
