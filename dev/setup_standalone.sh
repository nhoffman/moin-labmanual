#!/bin/bash

set -e

MOIN_VERSION=1.9.8

if [[ $1 == '--clean' ]]; then
    set -v
    rm -rf src/moin-${MOIN_VERSION} moin-env wiki wikiserver.py *.pyc pages.zip
    exit
fi

mkdir -p src
moin_src=moin-${MOIN_VERSION}.tar.gz
test -f src/$moin_src || \
    wget -P src -nc http://static.moinmo.in/files/$moin_src
tar -C src -xf src/$moin_src

test -d moin-env || virtualenv moin-env

# update pip
moin-env/bin/pip install -U pip

# install MoinMoin to the virtualenv
moin-env/bin/python -c 'import MoinMoin' 2> /dev/null || \
    moin-env/bin/pip install src/moin-${MOIN_VERSION}

# install other requirements
moin-env/bin/pip install -r requirements.txt

test -d wiki || cp -r src/moin-${MOIN_VERSION}/wiki .
ln -sf src/moin-${MOIN_VERSION}/wikiserver.py .
chmod +x wikiserver.py

# create pages.zip for installation to the wiki
./moinlm.py \
    package pages \
    -z wiki/underlay/pages/LanguageSetup/attachments/000-moinlm-pages.zip

# create user accounts

# username: testuser
# password: testpass
moin-env/bin/moin \
    --config-dir=$(pwd) \
    --wiki-url=http://localhost \
    account create \
    --name=testuser \
    --password=testpass \
    --email=testuser@nowhere.com

# username: superuser
# password: superpass
moin-env/bin/moin \
    --config-dir=$(pwd) \
    --wiki-url=http://localhost \
    account create \
    --name=superuser \
    --password=superpass \
    --email=superuser@nowhere.com



