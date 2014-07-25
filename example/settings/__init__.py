
import os

import cbs

mode = os.environ.get('DJANGO_MODE', 'Local')

cbs.apply('settings.{}.{}Settings'.format(mode.lower(), mode.title()), globals())
