#!/usr/bin/env python

"""Add-ons to MoinMoin for use in the clinical laboratory

"""

import argparse
import logging
import sys
import textwrap

from moinlm import __version__

log = logging


class Subparser(object):
    def __init__(self, subparsers, name):
        self.subparser = subparsers.add_parser(
            name,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            help=self.__doc__.strip().split('\n')[0],
            description=textwrap.dedent(self.__doc__.rstrip()))
        self.subparser.set_defaults(func=self.action)
        self.add_arguments()


class Nothing(Subparser):
    """
    Do nothing.

    """

    def add_arguments(self):
        self.subparser.add_argument(
            'infile', help="name of infile")

    def action(self, args):
        print args


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
    Nothing(subparsers, name='nothing')

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
