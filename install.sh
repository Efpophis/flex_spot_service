#!/bin/bash

mkdir -p /usr/local/scripts
sudo install -m755 spot_rpt /usr/local/scripts
sudo install net-efpophis-spots.service /etc/systemd/system

sudo systemctl enable net-efpophis-spots.service