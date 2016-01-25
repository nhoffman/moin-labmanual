import os
import subprocess
from setuptools import setup, find_packages

subprocess.call(
    ('mkdir -p moinlm/data && '
     'git describe --tags --dirty > moinlm/data/ver.tmp'
     '&& mv moinlm/data/ver.tmp moinlm/data/ver '
     '|| rm -f moinlm/data/ver.tmp'),
    shell=True, stderr=open(os.devnull, "w"))

from moinlm import __version__

setup(
    author='Noah Hoffman',
    author_email='ngh2@uw.edu',
    description='Add-ons to MoinMoin for use in the clinical laboratory',
    url='https://bitbucket.org/uwlabmed/moinlm',
    name='moinlm',
    packages=find_packages(),
    package_dir={'moinlm': 'moinlm'},
    package_data={'moinlm': ['data/ver']},
    entry_points={'console_scripts': ['moinlm = moinlm.cli:main']},
    version=__version__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
    ])
