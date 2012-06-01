import os

from fabric.api import run, sudo, cd, env, task

from ..templates import Template
from ..conf import setup_paths


@task
def install():
    print('Installing apache and mod-wsgi')
    
    sudo('apt-get install -y apache2 libapache2-mod-wsgi')
    # Get rid of Apache's default site
    sudo('a2dissite default')
    reload_webserver()


@task
def install_site(**kwargs):
    print('Adding Mayan EDMS\'s virtualhost file to apache')

    setup_paths(**kwargs)
    #TODO: mod site with paths
    sudo('cp %s /etc/apache2/sites-available/' % os.path.join(env.repository_path, 'contrib/apache/mayan'))
    sudo('a2ensite mayan') 


@task
def remove_site():
    sudo('a2dissite mayan')


@task    
def restart():
    print('Restarting the web server')
    
    sudo('/etc/init.d/apache2 restart')


@task
def reload():
    print('Reloading the web server')

    sudo('/etc/init.d/apache2 reload')
