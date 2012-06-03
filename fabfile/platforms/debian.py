from fabric.api import run, sudo, cd, env, task, settings

from ..literals import DB_MYSQL, WEB_APACHE


def install_dependencies():
    """
    Install Debian dependencies
    """
    sudo('apt-get install -y git-core gcc tesseract-ocr unpaper python-virtualenv ghostscript libjpeg-dev libpng-dev poppler-utils python-dev')


def install_database_manager():
    """
    Install the database manager on an Ubuntu system
    """

    if env.database_manager == DB_MYSQL:
        sudo('apt-get install -y mysql-server libmysqlclient-dev')
        
        with cd(env.virtualenv_path):
            sudo('source bin/activate; pip install MySQL-python')


def install_webserver():
    """
    Installing the Debian packages for the webserver
    """
   
    if env.webserver == WEB_APACHE:
        sudo('apt-get install -y apache2 libapache2-mod-wsgi')
        
        with settings(warn_only=True):
            # Get rid of Apache's default site
            sudo('a2dissite default')


def fix_permissions():
    """
    Fix installation files' permissions on a Debian system
    """
    sudo('chmod 770 %s -R' % env.virtualenv_path)
    sudo('chgrp www-data %s -R' % env.virtualenv_path)


def post_install():
    """
    Post install operations on a Debian system
    """    
    pass
