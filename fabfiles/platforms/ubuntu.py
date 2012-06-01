from fabric.api import run, sudo, cd, env, task

from ..conf import setup_paths

@task
def install_dependencies():
    print('Installing dependencies')

    sudo('apt-get install -y git-core gcc tesseract-ocr unpaper python-virtualenv ghostscript libjpeg-dev libpng-dev poppler-utils')


@task
def uninstall(**kwargs):
    drop_database=kwargs.pop('drop_database', False)
    setup_paths(**kwargs)
    print('Uninstalling Mayan EDMS from: %s' % env.virtualenv_path)

    sudo('rm %s -Rf' % env.virtualenv_path)
    
    if drop_database:
        #TODO: drop database
        pass

@task
def fix_permissions(**kwargs):
    setup_paths(**kwargs)
    
    sudo('chmod 777 %s -R' % env.virtualenv_path)
    sudo('chgrp www-data %s -R' % env.virtualenv_path)


@task
def install_mayan():
    print('Installing Mayan EDMS from git repository')
 
    with cd(env.install_path):
        sudo('virtualenv --no-site-packages %s' % env.virtualenv_name)
    
    with cd(env.virtualenv_path):
        sudo('git clone http://www.github.com/rosarior/mayan %s' % env.repository_name)
        sudo('source bin/activate; pip install -r %s/requirements/production.txt' % env.repository_name)


@task
def syncdb(**kwargs):
    setup_paths(**kwargs)

    with cd(env.virtualenv_path):
        sudo('source bin/activate; %(repository_name)s/manage.py syncdb --noinput; %(repository_name)s/manage.py migrate' % (env))
    
