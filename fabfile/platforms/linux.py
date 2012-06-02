from fabric.api import run, sudo, cd, env, task, settings


def delete_mayan():
    """
    Delete Mayan EDMS files from an Ubuntu system
    """
    sudo('rm %s -Rf' % env.virtualenv_path)
    

def install_mayan():
    """
    Install Mayan EDMS on an Ubuntu system
    """
    with cd(env.install_path):
        sudo('virtualenv --no-site-packages %s' % env.virtualenv_name)
    
    with cd(env.virtualenv_path):
        sudo('git clone http://www.github.com/rosarior/mayan %s' % env.repository_name)
        sudo('source bin/activate; pip install -r %s/requirements/production.txt' % env.repository_name)
