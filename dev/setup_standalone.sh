#!/bin/bash

MOIN_VERSION=1.9.8

if [[ $1 == '--clean' ]]; then
    set -v
    rm -rf src/moin-${MOIN_VERSION} moin-env wiki wikiserver.py *.pyc pages.zip
    exit
fi

mkdir -p src
wget -P src -N http://static.moinmo.in/files/moin-${MOIN_VERSION}.tar.gz
tar -C src -xf src/moin-${MOIN_VERSION}.tar.gz

test -d moin-env || virtualenv moin-env

moin-env/bin/python -c 'import MoinMoin' 2> /dev/null || \
    moin-env/bin/pip install src/moin-${MOIN_VERSION}

test -d wiki || cp -r src/moin-${MOIN_VERSION}/wiki .
ln -sf src/moin-${MOIN_VERSION}/wikiserver.py .
chmod +x wikiserver.py

# create pages.zip for installation to the wiki
./moinlm.py package -z wiki/underlay/pages/LanguageSetup/attachments/000-moin-labmanual.zip

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



