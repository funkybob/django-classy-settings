'''
URL style config parsing.

Inspired by dj_database_url
'''
from urllib.parse import parse_qs, unquote, urlparse

from .cast import as_bool

ENGINE_MAP = {
    'postgres': 'django.db.backends.postgresql',
    'postgresql': 'django.db.backends.postgresql',
    'mysql': 'django.db.backends.mysql',
    'mariadb': 'django.db.backends.mysql',
    'sqlite': 'django.db.backends.sqlite3',
    'oracle': 'django.db.backends.oracle',
}

OPTS = {
    'ATOMIC_REQUESTS': as_bool,
    'AUTOCOMMIT': as_bool,
    'CONN_MAX_AGE': int,
    'CONN_HEALTH_CHECKS': as_bool,
    'TIME_ZONE': str,
    'DISABLE_SERVER_SIDE_CURSORS': as_bool,
    'CHARSET': str,
    'COLLATION': str,
}


def parse_dburl(url: str) -> dict:
    url = urlparse(url)

    config = {
        "ENGINE": ENGINE_MAP.get(url.scheme, url.scheme),
        "NAME": unquote(url.path or "").lstrip('/'),
        "USER": unquote(url.username or ""),
        "PASSWORD": unquote(url.password or ""),
        "HOST": url.hostname,
        "PORT": str(url.port) if url.port else None,
    }

    opts = parse_qs(url.query)

    options = {}

    for key, values in opts.items():
        _key = key.upper()
        try:
            caster = OPTS[_key]
            config[_key] = caster(*values)
        except KeyError:
            options[key] = values[0]

    if options:
        config['OPTIONS'] = options

    return config
