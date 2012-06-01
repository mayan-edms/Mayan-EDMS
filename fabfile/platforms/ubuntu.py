from fabric.api import run, sudo, cd, env, task

from ..literals import DB_MYSQL, WEB_APACHE


def install_dependencies():
    """
    Install Ubuntu dependencies
    """
    sudo('apt-get install -y git-core gcc tesseract-ocr unpaper python-virtualenv ghostscript libjpeg-dev libpng-dev poppler-utils')


def uninstall():
    """
    Uninstall Mayan EDMS from an Ubuntu system
    """
    sudo('rm %s -Rf' % env.virtualenv_path)
    

def fix_permissions():
    """
    Fix installation files' permissions on an Ubuntu system
    """
    sudo('chmod 777 %s -R' % env.virtualenv_path)
    sudo('chgrp www-data %s -R' % env.virtualenv_path)


def install_mayan():
    """
    Install Mayan EDMS on an Ubuntu system
    """
    with cd(env.install_path):
        sudo('virtualenv --no-site-packages %s' % env.virtualenv_name)
    
    with cd(env.virtualenv_path):
        sudo('git clone http://www.github.com/rosarior/mayan %s' % env.repository_name)
        sudo('source bin/activate; pip install -r %s/requirements/production.txt' % env.repository_name)


def install_database_manager():
    """
    Install the database manager on an Ubuntu system
    """

    if env.database_manager == DB_MYSQL:
        sudo('apt-get install -y mysql-server libmysqlclient-dev')
        
        with cd(env.virtualenv_path):
            sudo('source bin/activate; pip install MySQL-python')


@task
def install_webserver():
    """
    Installing the Ubuntu packages for the webserver
    """
   
    if env.webserver == WEB_APACHE:
        sudo('apt-get install -y apache2 libapache2-mod-wsgi')
        
        with settings(warn_only=True):
            # Get rid of Apache's default site
            sudo('a2dissite default')
