#!/bin/bash

rm -rf build
rm -rf dist
rm -rf spot_rpt
rm -f spot_rpt.spec

# stupid windows
if [ "`uname`" == "Linux" ]; then
    pyinstaller --onefile --noconsole spot_rpt.py
else
    python -m PyInstaller --onefile --noconsole spot_rpt.py
fi

cp net-efpophis-spots.service dist

mkdir -p spot_rpt
cp install.sh spot_rpt
cp uninstall.sh spot_rpt
cp -r dist spot_rpt

tar cvfz spot_rpt.tar.gz spot_rpt
rm -rf spot_rpt
