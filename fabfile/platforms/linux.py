from fabric.api import run, sudo, cd, env, task, settings


def delete_mayan():
    """
    Delete Mayan EDMS files from an Ubuntu system
    """
    sudo('rm %(virtualenv_path)s -Rf' % env)
    

def install_mayan():
    """
    Install Mayan EDMS on an Ubuntu system
    """
    with cd(env.install_path):
        sudo('virtualenv --no-site-packages %(virtualenv_name)s' % env)
    
    with cd(env.virtualenv_path):
        sudo('git clone git://github.com/rosarior/mayan.git %(repository_name)s' % env)
        sudo('source bin/activate; pip install -r %(repository_name)s/requirements/production.txt' % env)
