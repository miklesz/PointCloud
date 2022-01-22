#!/bin/sh
python setup.py build_apps
cd build
zip -r '/Users/miklesz/Dysk Google/Demo/build/macosx_10_9_x86_64.zip' macosx_10_9_x86_64
zip -r '/Users/miklesz/Dysk Google/Demo/build/manylinux1_x86_64.zip' manylinux1_x86_64
zip -r '/Users/miklesz/Dysk Google/Demo/build/win_amd64.zip' win_amd64
