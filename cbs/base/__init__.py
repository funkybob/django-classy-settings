
import inspect
import os


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

    ALLOWED_HOSTS = []

    @property
    def ROOT_URLCONF(self):
        return '{}.urls'.format(self.PROJECT_NAME)

    @property
    def WSGI_APPLICATION(self):
        return '{}.wsgi.application'.format(self.PROJECT_NAME)


class GlobalSettings(object):

    def __getattr__(self, key):
        from django.conf import global_settings
        return getattr(global_settings, key)
