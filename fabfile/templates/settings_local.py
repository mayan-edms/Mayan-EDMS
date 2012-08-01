DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.%(django_database_driver)s',
        'NAME': '%(database_name)s',
        'USER': '%(database_username)s',
        'PASSWORD': '%(database_password)s',
        'HOST': '%(database_host)s',
        'PORT': '',
    }
}
