# invoke gunicorn using
# 'gunicorn -c <this_file> <project_module>.wsgi:application
import os
import multiprocessing

from django.conf import settings

bind = settings.GUNICORN_BIND
workers = multiprocessing.cpu_count() * 2 + 1

preload_app = True

chdir = settings.BASE_DIR

user = settings.PROCESS_USER
group = user

log_dir = os.path.join(
    os.path.dirname(settings.BASE_DIR), 'gunicorn_logs', settings.PROCESS_NAME)
if not os.path.isdir(log_dir):
    os.makedirs(log_dir)
    import pwd
    import grp
    os.chown(log_dir,
             pwd.getpwnam(user).pw_uid,
             grp.getgrnam(group).gr_gid)

accesslog = os.path.join(log_dir, 'access.log')
errorlog = os.path.join(log_dir, 'error.log')

proc_name = settings.PROCESS_NAME