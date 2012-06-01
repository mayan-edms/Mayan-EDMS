import os

from fabric.api import env, task, cd, sudo
from fabric.contrib.files import upload_template


@task
def syncdb():
    with cd(env.virtualenv_path):
        sudo('source bin/activate; %(repository_name)s/manage.py syncdb --noinput; %(repository_name)s/manage.py migrate' % (env))

@task
def database_config():
    upload_template(filename=os.path.join('fabfile', 'templates', 'settings_local.py'), destination=env.repository_path, context=env, use_sudo=True)
