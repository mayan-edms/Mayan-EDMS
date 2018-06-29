#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import mayan

PACKAGE_NAME = 'mayan-edms'
PACKAGE_DIR = 'mayan'

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)


def find_packages(directory):
    # Compile the list of packages available, because distutils doesn't have
    # an easy way to do this.
    packages, data_files = [], []
    root_dir = os.path.dirname(__file__)
    if root_dir != '':
        os.chdir(root_dir)

    for dirpath, dirnames, filenames in os.walk(directory):
        if not dirpath.startswith('mayan/media'):
            # Ignore dirnames that start with '.'
            if os.path.basename(dirpath).startswith('.'):
                continue
            if '__init__.py' in filenames:
                packages.append('.'.join(fullsplit(dirpath)))
            elif filenames:
                data_files.append(
                    [dirpath, [os.path.join(dirpath, f) for f in filenames]]
                )

    return packages

install_requires = """
Django==1.11.11
Pillow==5.0.0
PyYAML==3.12
celery==3.1.24
cssmin==0.2.0
django-activity-stream==0.6.5
django-autoadmin==1.1.1
django-celery==3.2.1
django-colorful==1.2
django-compressor==2.2
django-cors-headers==2.2.0
django-downloadview==1.9
django-environ==0.4.4
django-formtools==2.1
django-pure-pagination==0.3.0
django-mathfilters==0.4.0
django-model-utils==3.1.1
django-mptt==0.9.0
django-qsstats-magic==1.0.0
django-stronghold==0.3.0
django-suit==0.2.26
django-widget-tweaks==1.4.1
djangorestframework==3.7.7
djangorestframework-recursive==0.1.2
drf-yasg==1.5.0
flanker==0.8.5
flex==6.12.0
furl==1.0.1
fusepy==2.0.4
gevent==1.2.2
graphviz==0.8.2
gunicorn==19.7.1
mock==2.0.0
node-semver==0.3.0
pathlib==1.0.1
pycountry==18.5.26
PyPDF2==1.26.0
pyocr==0.5.1
python-dateutil==2.6.1
python-gnupg==0.3.9
python-magic==0.4.15
pytz==2018.3
requests==2.18.4
sh==1.12.14
swagger-spec-validator==2.1.0
whitenoise==3.3.1
""".split()

with open('README.rst') as f:
    readme = f.read()

with open('HISTORY.rst') as f:
    history = f.read()

setup(
    author='Roberto Rosario',
    author_email='roberto.rosario@mayan-edms.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Communications :: File Sharing',
    ],
    description='Free Open Source Electronic Document Management System',
    include_package_data=True,
    install_requires=install_requires,
    license='Apache 2.0',
    long_description=readme + '\n\n' + history,
    name=PACKAGE_NAME,
    packages=find_packages(PACKAGE_DIR),
    platforms=['any'],
    scripts=['mayan/bin/mayan-edms.py'],
    url='https://gitlab.com/mayan-edms/mayan-edms',
    version=mayan.__version__,
    zip_safe=False,
)
