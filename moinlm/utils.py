"""Various utility functions

"""

from collections import OrderedDict
from itertools import groupby, izip_longest
from operator import attrgetter

# from MoinMoin.Page import Page
# from MoinMoin.PageEditor import PageEditor
from MoinMoin import wikiutil


def parse_args(argstr, posargs=None, **kwargs):
    """

    * argstr - a unicode string from which to parse arguments
    * posargs - a list of positional arguments
    * kwargs - optional keywords and default values are provided as key=value
    """

    argstr = argstr or u''
    posargs = posargs or []
    positional, keyvalue, trailing = wikiutil.parse_quoted_separated(argstr or u'')

    # in the absence of positional arguments 'positional' is '[None]'
    positional = [x for x in positional if x is not None]

    if len(positional) > len(posargs):
        raise ValueError(
            'Too many positional arguments - expected {}, got {}'.format(
                len(posargs), len(positional)))

    # start with positional arguments and defaults in kwargs
    argv = dict(izip_longest(posargs, positional), **kwargs)

    # update using any keyword arguments
    argv.update(keyvalue)

    # make sure that all posargs arguments are provided
    if set(posargs) > set(argv.keys()):
        raise ValueError('Missing arguments: {}'.format(
            set(posargs) - set(argv.keys())))

    # raise an error if there are unexpected keyword arguments in argstr
    if set(argv.keys()) > set(posargs + kwargs.keys()):
        raise ValueError('One or more unexpected keywords: {}'.format(
            ','.join(set(argv.keys()) - set(posargs + kwargs.keys()))))

    return argv


def pivot(rows, rowattr, colattr, cellfun=None, nullval=None, colnames=None):
    """Create a table in "wide" format given a sequence of objects with
    attributes 'rowattr' and 'colattr'. 'cellfun' is applied to each
    row to provide the value appearing in each cell. The upper left
    corner of the table is 'nullval'. Column names may be specified by
    'colnames', defining a subset or superset of names appearing in
    rows. If colnames is a list, the order will be preserved.

    """

    rowgetter = attrgetter(rowattr)
    colgetter = attrgetter(colattr)
    cellfun = cellfun or (lambda row: None)

    if colnames and isinstance(colnames, list):
        colnames = OrderedDict((c, None) for c in colnames)
    elif colnames:
        colnames = OrderedDict((c, None) for c in sorted(colnames))
    else:
        colnames = OrderedDict(
            (c, None) for c in sorted(colgetter(row) for row in rows))

    # colnames = sorted(set(colgetter(row) for row in rows))

    # iterator of (rowname, {colname: cellval, ...})
    pivot = ((rowname,
              {colgetter(row): cellfun(row) for row in grp})
             for rowname, grp in groupby(sorted(rows, key=rowgetter), rowgetter))

    yield [nullval] + colnames.keys()
    for rowname, data in pivot:
        yield [rowname] + [data.get(colname, nullval) for colname in colnames]
