import os

from fabric.api import run, sudo, cd, env, task


def install_site():
    """
    Install Mayan EDMS's site file in Apache configuration
    """

    #TODO: mod site with paths
    sudo('cp %s /etc/apache2/sites-available/' % os.path.join(env.repository_path, 'contrib/apache/mayan'))
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
