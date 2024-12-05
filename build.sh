#!/bin/bash

rm -rf build
rm -rf dist
rm -f spot_rpt.spec

python -m PyInstaller --onefile --noconsole spot_rpt.py
cp net-efpophis-spots.service dist
