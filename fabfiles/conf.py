import os

from fabric.api import run, sudo, cd, env, task

from literals import DEFAULT_INSTALL_PATH, DEFAULT_VIRTUALENV_NAME, DEFAULT_REPOSITORY_NAME, DEFAULT_OS


def setup_paths(**kwargs):
    env['os'] = kwargs.pop('os', DEFAULT_OS)
    env['install_path'] = kwargs.pop('path', DEFAULT_INSTALL_PATH[env.os])
    env['virtualenv_name'] = kwargs.pop('virtualenv_name', DEFAULT_VIRTUALENV_NAME[env.os])
    env['repository_name'] = kwargs.pop('repository_name', DEFAULT_REPOSITORY_NAME[env.os])
    env['virtualenv_path'] = os.path.join(env.install_path, env.virtualenv_name)
    env['repository_path'] = os.path.join(env.virtualenv_path, env.repository_name) 
