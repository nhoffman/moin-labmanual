#!/bin/bash

MOIN_VERSION=1.9.8

mkdir -p src

(cd src && \
	wget -N http://static.moinmo.in/files/moin-${MOIN_VERSION}.tar.gz && \
	tar -xf moin-${MOIN_VERSION}.tar.gz)

test -d moin-env || virtualenv moin-env
moin-env/bin/pip install src/moin-${MOIN_VERSION}

# create a user account:
# username: testuser
# password: testpass

moin-env/bin/moin \
    --config-dir=src/moin-${MOIN_VERSION} \
    --wiki-url=http://localhost \
    account create \
    --name=testuser \
    --password=testpass \
    --email=testuser@nowhere.com

# http://localhost:8080/LanguageSetup?action=language_setup&target=English--all_pages.zip&language=English
