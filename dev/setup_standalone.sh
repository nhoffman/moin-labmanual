#!/bin/bash

MOIN_VERSION=1.9.8

mkdir -p src
wget -P src -N http://static.moinmo.in/files/moin-${MOIN_VERSION}.tar.gz
tar -C src -xf src/moin-${MOIN_VERSION}.tar.gz

test -d moin-env || virtualenv moin-env

moin-env/bin/python -c 'import MoinMoin' 2> /dev/null || \
    moin-env/bin/pip install src/moin-${MOIN_VERSION}

test -d wiki || cp -r src/moin-${MOIN_VERSION}/wiki .
cp -r src/moin-${MOIN_VERSION}/wiki/wikiserver.py .
chmod +x wikiserver.py

# create a user account:
# username: testuser
# password: testpass

moin-env/bin/moin \
    --config-dir=$(pwd) \
    --wiki-url=http://localhost \
    account create \
    --name=testuser \
    --password=testpass \
    --email=testuser@nowhere.com


