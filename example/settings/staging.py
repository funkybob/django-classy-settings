
from .base import BaseSettings

import os


class StagingSettings(BaseSettings):

    DOCROOT = '/path/to/docroot/'

    def STATIC_ROOT(self):
        return os.path.join(self.DOCROOT, 'static', '')

    def MEDIA_ROOT(self):
        return os.path.join(self.DOCROOT, 'media', '')
