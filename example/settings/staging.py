
from .base import BaseSettings

import os

class StagingSettings(BaseSettings):

    DOCROOT = '/path/to/docroot/'

    @property
    def STATIC_ROOT(self):
        return os.path.join(self.DOCROOT, 'static', '')

    @property
    def MEDIA_ROOT(self):
        return os.path.join(self.DOCROOT, 'media', '')

