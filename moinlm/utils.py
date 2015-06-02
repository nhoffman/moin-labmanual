"""Various utility functions

"""

from itertools import izip_longest

# from MoinMoin.Page import Page
# from MoinMoin.PageEditor import PageEditor
from MoinMoin import wikiutil


def parse_args(argstr, required=None, **kwargs):
    """

    * argstr - a unicode string from which to parse arguments
    * required - a list of required arguments
    * kwargs - optional keywords and default values are provided as key=value
    """

    required = required or []
    positional, keyvalue, trailing = wikiutil.parse_quoted_separated(argstr or u'')

    # in the absence of positional arguments 'positional' is '[None]'
    positional = [x for x in positional if x is not None]

    if len(positional) > len(required):
        raise ValueError(
            'Too many positional arguments - expected {}, got {}'.format(
                len(required), len(positional)))

    # start with positional arguments and defaults in kwargs
    argv = dict(izip_longest(required, positional), **kwargs)

    # update using any keyword arguments
    argv.update(keyvalue)

    # make sure that all required arguments are provided
    if set(required) > set(argv.keys()):
        raise ValueError('Missing arguments: {}'.format(
            set(required) - set(argv.keys())))

    # raise an error if there are unexpected keyword arguments in argstr
    if set(argv.keys()) > set(required + kwargs.keys()):
        raise ValueError('One or more unexpected keywords: {}'.format(
            ','.join(set(argv.keys()) - set(required + kwargs.keys()))))

    return argv
