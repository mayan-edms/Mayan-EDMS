import os

from fabric.api import env, task, cd, sudo
from fabric.contrib.files import upload_template

from ..conf import setup_environment


@task
def syncdb():
    """
    Perform Django's syncdb command
    """
    setup_environment()
    with cd(env.virtualenv_path):
        sudo('source bin/activate; %(repository_name)s/manage.py syncdb --noinput; %(repository_name)s/manage.py migrate' % (env))

@task
def database_config():
    """
    Create a settings_local.py file tailored to the database manager selected
    """
    setup_environment()
    upload_template(filename=os.path.join('fabfile', 'templates', 'settings_local.py'), destination=env.repository_path, context=env, use_sudo=True)


@task
def collectstatic():
    """
    Perform Django's collectstatic command
    """
    setup_environment()
    with cd(env.virtualenv_path):
        sudo('source bin/activate; %(repository_name)s/manage.py collectstatic --noinput' % (env))
