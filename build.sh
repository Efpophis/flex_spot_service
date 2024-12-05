#!/bin/bash

rm -rf build
rm -rf dist
rm -rf spot_rpt
rm -f spot_rpt.spec


python -m PyInstaller --onefile --noconsole spot_rpt.py
cp net-efpophis-spots.service dist

mkdir -p spot_rpt
cp install.sh spot_rpt
cp -r dist spot_rpt

tar cvfz spot_rpt.tar.gz spot_rpt