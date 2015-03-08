from os import path

try:
    with open(path.join(path.dirname(__file__), 'data', 'ver')) as f:
        __version__ = f.read().strip()
except Exception, e:
    __version__ = ''

plugin_dir = path.join(path.dirname(__file__), 'plugin')
