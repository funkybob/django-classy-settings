

def as_bool(value):
    '''
    Smart cast value to bool
    '''
    if isinstance(value, bool):
        return value
    value = value.strip().lower()
    if value in ('y', 'yes', 'on', 't', 'true', '1'):
        return True
    if value in ('n', 'no', 'off', 'f', 'false', '0'):
        return False
    raise ValueError('Unrecognised value for bool: %r' % value)
