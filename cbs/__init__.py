
from functools import partial
import importlib
import inspect
import os

from django.utils import six


DEFAULT_ENV_PREFIX = ''


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

    def __init__(self, getter, key=None, prefix=DEFAULT_ENV_PREFIX):
        self.getter = getter
        key = key or getter.__name__
        self.key = ''.join([prefix, key])

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        try:
            value = os.environ[self.key]
        except KeyError:
            value = self.getter(self)
        obj.__dict__[self.getter.__name__] = value
        return value


class envbool(env):
    '''
    A special case of env that returns a boolean.
    '''
    def __get__(self, obj, type=None):
        value = super(envbool, self).__get__(obj, type=type)
        if isinstance(value, bool):
            return value
        value = value.strip().lower()
        if value in ('y', 'yes', 'on', 't', 'true', '1'):
            return True
        if value in ('n', 'no', 'off', 'f', 'false', '0'):
            return False
        raise ValueError('Unrecognised value for bool: %r' % value)


def apply(name, to):
    '''
    Apply settings to ``to``, which is expected to be globals().

    Place at the end of settings.py / settings/__init__.py to apply a given
    settings class.

    Pass a settings class:
        cbs.apply(MySettings, globals())

    Pass a class name:
        cbs.apply('MySettings', globals())

    Pass an import path:
        cbs.apply('settings.my.MySettings', globals())

    '''
    if isinstance(name, six.string_types):
        if '.' in name:
            module, obj_name = name.rsplit('.', 1)
            module = importlib.import_module(module)
            obj = getattr(module, obj_name)
        else:
            obj = to.get(name)
    else:
        obj = name

    if obj is None:
        raise ValueError('Could not find settings class: %r', name)

    settings = obj()

    def resolve_callable(value):
        if callable(value):
            return value()
        return value

    to.update({
        key: resolve_callable(getattr(settings, key))
        for key in dir(settings)
        if key == key.upper()
    })


class CoreSettings(object):
    '''
    Settings not likely to change between versions
    '''

    @property
    def BASE_DIR(self):
        return os.path.dirname(
            os.path.dirname(
                os.path.abspath(inspect.getfile(self.__class__))
            )
        )

    DEBUG = True

    @property
    def TEMPLATE_DEBUG(self):
        return self.DEBUG

    ALLOWED_HOSTS = []

    @property
    def ROOT_URLCONF(self):
        return '{}.urls'.format(self.PROJECT_NAME)

    @property
    def WSGI_APPLICATION(self):
        return '{}.wsgi.application'.format(self.PROJECT_NAME)


class Base16Settings(CoreSettings):
    '''
    A standard Django 1.6 setting

    You must sub-class this and define PROJECT_NAME
    '''

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

    # Database
    # https://docs.djangoproject.com/en/1.6/ref/settings/#databases

    @property
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


class Base17Settings(CoreSettings):

    # Application definition

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
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    # Database
    # https://docs.djangoproject.com/en/1.7/ref/settings/#databases

    @property
    def DATABASES(self):
        return {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(self.BASE_DIR, 'db.sqlite3'),
            }
        }

    # Internationalization
    # https://docs.djangoproject.com/en/1.7/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.7/howto/static-files/

    STATIC_URL = '/static/'


from django import VERSION

BASE_MAP = {
    (1, 6): Base16Settings,
    (1, 7): Base17Settings,
}
BaseSettings = BASE_MAP.get(VERSION[:2], Base16Settings)
