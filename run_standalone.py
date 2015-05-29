#!/usr/bin/env python

"""Launch the standalone server.

Enter CTRL-C once to restart, twice to exit.

"""

import signal
import sys
import subprocess


def handler(signum, frame):
    try:
        raw_input('\nEnter Return to restart, or CTRL-C to exit: ')
    except RuntimeError:
        sys.exit()
    else:
        print '\n*** Restarting server ***\n'

signal.signal(signal.SIGINT, handler)

print __doc__

while True:
    subprocess.call(['./wikiserver.py'])
