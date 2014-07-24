
from functools import partial
import importlib
import os.environ
import six

from django.conf import global_settings, UserSettingsHolder, settings


class env(object):
    '''
    Decorator to make environ based settings simpler.

    @env
    def SOMETHING_KEY(self):
        return 'default'

    You can override the key to use in the env:


    @env(key='OTHER_NAME')
    def SETTINGS_NAME(self):
        ...

    Or, if you want the env to have a prefix not in settings:

    @env(prefix='MY_')
    def SETTING(self):
        ...

    ``key`` and ``prefix`` can be used together.
    '''
    def __new__(cls, *args, **kwargs):
        if not args:
            return partial(env, **kwargs)
        return object.__new__(cls)

    def __init__(self, getter, key=None, prefix=None):
        self.getter = getter
        key = key or getter.__name__
        self.key = key if prefix is None else ''.join([prefix, key])

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        try:
            value = os.environ[self.key]
        except KeyError:
            value = self.getter()
        obj.__dict__[self.getter.__name__] = value
        return value


def activate(name):
    '''
    specify which settings to use.

    Uses:
    Pass a settings class:
        cbs.activate(MySettings)

    Pass the name of a local settings class:
        cbs.activate('MySettings')

    Pass an import path:
        cbs.activate('settings.MySettings')
    '''
    if isinstance(name, six.string_types):
        if '.' in name:
            module, name = name.rsplit('.')
            module = importlib.import_module(module)
            obj = getattr(module, name)
        else:
            obj = globals().get(name)
    else:
        obj = name

    settings._wrapped = obj(global_settings)


class BaseSettings(UserSettingsHolder):
    '''
    A standard Django 1.6 setting

    You must sub-class this and define PROJECT_NAME
    '''

    DEBUG = True

    @property
    def BASE_DIR(self):
        return os.path.dirname(os.path.dirname(self.__class__.__file__))

    @property
    def TEMPLATE_DEBUG(self):
        return self.DEBUG

    ALLOWED_HOSTS = []

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    )

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    @property
    def ROOT_URLCONF(self):
        return '{}.urls'.format(self.PROJECT_NAME)

    @property
    def WSGI_APPLICATION(self):
        return '{}.wsgi.application'.format(self.PROJECT_NAME)

    # Database
    # https://docs.djangoproject.com/en/1.6/ref/settings/#databases

    @properties
    def DATABASES(self):
        return {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(self.BASE_DIR, 'db.sqlite3'),
            }
        }

    # Internationalization
    # https://docs.djangoproject.com/en/1.6/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.6/howto/static-files/

    STATIC_URL = '/static/'
