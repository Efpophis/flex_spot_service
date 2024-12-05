#!/bin/bash

sudo systemctl disable net-efpophis-spots
sudo rm -f /etc/systemd/system/net-efpophis-spots.service
sudo rm -f /usr/local/scripts/spot_rpt
