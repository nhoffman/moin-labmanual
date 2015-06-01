#!/usr/bin/env python

"""Add-ons to MoinMoin for use in the clinical laboratory

"""

import argparse
import logging
import sys
import textwrap
import zipfile
import glob
import csv
from itertools import chain, groupby, count
from os import path

from moinlm import __version__

log = logging.getLogger(__name__)


class Subparser(object):
    def __init__(self, subparsers, name):
        self.subparser = subparsers.add_parser(
            name,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            help=self.__doc__.strip().split('\n')[0],
            description=textwrap.dedent(self.__doc__.rstrip()))
        self.subparser.set_defaults(func=self.action)
        self.add_arguments()


class Package(Subparser):
    """Create a package of pages.

    Each directory in ``pages_dir`` should contain wiki pages as plain
    text files. Each file may end with an optional revision number
    (eg, PageName.1). Multiple revisions of a page may be provided by
    naming files PageName.1, PageName.2, etc. An author name and
    revision comment may be provided for each revision in a file
    ending with '.revisions' (eg PageName.revisions) in the format
    'revision|author|comment'.

    See HelpOnPackageInstaller
    """

    def page_group(self, grp):
        """Given an iterable of page names, returns (pages, data), where pages
        is a list of filenames in grp not ending with '.revisions',
        and data is a dict in the format {revision: (author, comment)}
        if a file ending with '.revisions' exists, else {}.

        """
        grp = list(grp)
        revs = [grp.pop(i) for i, f in enumerate(grp) if f.endswith('.revisions')]
        if revs:
            with open(revs[0]) as f:
                # revision|author|comment
                data = {r: (a, c) for r, a, c in csv.reader(f, delimiter='|')}
        else:
            data = {}

        return grp, data

    def add_arguments(self):
        self.subparser.add_argument(
            'pages_dir', default='pages', help="directory containing pages",
            nargs='*')
        self.subparser.add_argument(
            '-z', '--zipfile', default='pages.zip',
            help="name of output file (ends with .zip) [%(default)s]")

    def action(self, args):
        lines = ['MoinMoinPackage|1']
        pages = chain.from_iterable(glob.glob(path.join(pth, '*'))
                                    for pth in args.pages_dir)

        def pagename(pth):
            return path.basename(pth.split('.')[0])

        with zipfile.ZipFile(args.zipfile, 'w') as zf:
            counter = count(1)
            for pagename, grp in groupby(pages, key=pagename):

                pages, data = self.page_group(grp)
                for i, fn in enumerate(pages):
                    log.info(fn)
                    num = '{}'.format(next(counter))
                    zf.write(fn, num)

                    # Update the page manifest
                    # if i == 0:
                    #     # ReplaceUnderlay|filename|pagename
                    #     lines.append('|'.join(['ReplaceUnderlay', num, pagename]))

                    # AddRevision|filename|pagename|author|comment|trivial
                    try:
                        _, rev = fn.rsplit('.', 1)
                        rev = rev if rev.isdigit() else None
                    except ValueError:
                        rev = None

                    # if rev:
                    #     line = ['AddRevision', num, pagename]
                    #     # add comment, author if provided in pagename.revisions
                    #     if data and rev in data:
                    #         line.extend(data[rev])
                    #     lines.append('|'.join(line))

                    line = ['AddRevision', num, pagename]
                    # add comment, author if provided in pagename.revisions
                    if data and rev in data:
                        line.extend(data[rev])
                    lines.append('|'.join(line))

            log.info('\n' + '\n'.join(lines))
            zf.writestr('MOIN_PACKAGE', '\n'.join(lines))


class VersionAction(argparse._VersionAction):
    """Write the version string to stdout and exit"""
    def __call__(self, parser, namespace, values, option_string=None):
        formatter = parser._get_formatter()
        formatter.add_text(parser.version if self.version is None else self.version)
        sys.stdout.write(formatter.format_help())
        sys.exit(0)


def main(arguments=None):

    if arguments is None:
        arguments = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        '-v', action='count', dest='verbosity', default=1,
        help='increase verbosity of screen output (eg, -v is verbose, '
        '-vv more so)')
    parser.add_argument(
        '-q', '--quiet', action='store_const', dest='verbosity', const=0,
        help='suppress screen output from pip commands')
    parser.add_argument(
        '-V', '--version', action=VersionAction, version=__version__,
        help='Print the version number and exit')

    subparsers = parser.add_subparsers()
    Package(subparsers, name='package')

    args = parser.parse_args(arguments)

    # set up logging
    loglevel = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG,
    }.get(args.verbosity, logging.DEBUG)

    logformat = '%(levelname)s %(message)s' if args.verbosity > 1 else '%(message)s'
    logging.basicConfig(file=sys.stderr, format=logformat, level=loglevel)

    return args.func(args)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
