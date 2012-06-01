from fabric.api import run, sudo, cd, env, task


@task
def install_database_manager():
    print('Installing MySQL')

    sudo('apt-get install -y mysql-server libmysqlclient-dev')
    
    with cd(env.virtualenv_path):
        sudo('source bin/activate; pip install MySQL-python')


@task
def create_database(*args, **kwargs):
    print('Setting up Mayan EDMS\'s MySQL database')
    
    #TODO: create DB and mayan user
    #TODO: custom settings_local
    
