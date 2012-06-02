import os

from fabric.api import run, sudo, cd, env, task, settings
from fabric.operations import put, reboot

from ..literals import DB_MYSQL, WEB_APACHE


def install_dependencies():
    """
    Install Fedora dependencies
    """
    sudo('yum install -y git gcc tesseract unpaper python-virtualenv ghostscript libjpeg-turbo-devel libpng-devel poppler-utils')


def install_database_manager():
    """
    Install the database manager on a Fedora system
    """

    if env.database_manager == DB_MYSQL:
        sudo('yum install -y mysql-server mysql-devel')
        sudo('systemctl enable mysqld.service')
        sudo('systemctl start mysqld.service')
        sudo('mysql_secure_installation')
        
        with cd(env.virtualenv_path):
            sudo('source bin/activate; pip install MySQL-python')


def install_webserver():
    """
    Installing the Fedora packages for the webserver
    """
   
    if env.webserver == WEB_APACHE:
        sudo('yum install -y httpd mod_wsgi')
        sudo('systemctl enable httpd.service')
        sudo('systemctl start httpd.service')
        
        with settings(warn_only=True):
            # Get rid of Apache's default site
            sudo('rm /etc/httpd/conf.d/welcome.conf')
            
        # Disable SELinux as it blocks mod_wsgi's file access
        # TODO: implement a proper solution is implemented
        put(local_path=os.path.join('fabfile', 'templates', 'selinux.config'), remote_path='/etc/selinux/config',  use_sudo=True) 


def fix_permissions():
    """
    Fix installation files' permissions on a Fedora system
    """
    sudo('chmod 770 %s -R' % env.virtualenv_path)
    sudo('chgrp apache %s -R' % env.virtualenv_path)


def post_install():
    """
    Post install operations on a Fedora system
    """    
    reboot()
