#!/bin/bash

if [ -x build.sh ]; then
    ./build.sh
else
    echo "no build script. Can't continue"
    exit 1
fi

if [ -d dist ]; then    
    pushd dist
    mkdir -p /usr/local/scripts
    sudo install -m755 spot_rpt /usr/local/scripts
    sudo install net-efpophis-spots.service /etc/systemd/system

    sudo systemctl enable net-efpophis-spots.service
    popd
else
    echo "nothing to install (dist doesn't exist)"
    exit 1
fi