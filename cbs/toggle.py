'''
Hepler for defining feature toggles.
'''
import os

from .utils import as_bool


def toggles(**options):
    '''
    Produces a dict of {name: env(name, default)}
    '''
    return {
        name: as_bool(os.environ.get('TOGGLE_%s' % name, default))
        for name, default in options.items()
    }
