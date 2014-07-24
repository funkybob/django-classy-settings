
import os

from cbs import activate

mode = os.environ.get('DJANGO_MODE', 'Local')

activate('settings.{}.{}Settings'.format(mode.lower(), model.title()))

