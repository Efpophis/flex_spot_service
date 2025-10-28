#!/bin/bash

read -p "What is your call sign? " user_call
read -p "Which dxcluster host do you want to use? [dxusa.net] " cl_host
read -p "   Which port? [7300] " cl_port

if [ -z "$user_call" ]; then
    echo "You must specify your callsign"
    exit
fi

cl_host=${cl_host:-dxusa.net}
cl_port=${cl_port:-7300}

if [ -x build.sh ]; then
    ./build.sh
fi

if [ -d dist ]; then    
    pushd dist
    mkdir -p /usr/local/scripts
    sudo install -m755 spot_rpt /usr/local/scripts
    sudo install net-efpophis-spots.service /etc/systemd/system
    sudo install -m644 flex_spots.conf /usr/local/etc
    sudo sed -e "s/CLUSTER_HOST/$cl_host/g" -i /usr/local/etc/flex_spots.conf
    sudo sed -e "s/CLUSTER_PORT/$cl_port/g" -i /usr/local/etc/flex_spots.conf
    sudo sed -e "s/USER_CALLSIGN/$user_call/g" -i /usr/local/etc/flex_spots.conf

    sudo systemctl enable --now net-efpophis-spots.service
    sleep 2
    systemctl status net-efpophis-spots
    popd
else
    echo "nothing to install (dist doesn't exist)"
    exit 1
fi