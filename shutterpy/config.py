from configparser import ConfigParser


def _config():
    if '__config' not in globals():
        from shutterpy import resolve_path
        config = ConfigParser()
        config.read(resolve_path('.shutterpy/config.ini'))
        globals()['__config'] = config
    return globals()['__config']


def get(section, key):
    return _config().get(section, key)


def sections():
    return _config().sections()


def section(key, silent=False):
    if silent:
        return _config().get(key)
    else:
        return _config()[key]
