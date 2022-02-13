#!/bin/sh
# python3 setup.py build_apps
# python3-intel64 setup.py build_apps
# /Library/Frameworks/Python.framework/Versions/3.9/bin/python3.9-intel64 setup.py build_apps
# which python
python setup.py build_apps
cd build || exit
rm /Users/miklesz/Dysk\ Google/Demo/build/*.zip
DATE=`date`
DATE="${DATE// /_}"
zip -q -r '/Users/miklesz/Dysk Google/Demo/build/macosx_10_9_x86_64_'$DATE'.zip' macosx_10_9_x86_64
zip -q -r '/Users/miklesz/Dysk Google/Demo/build/manylinux2010_x86_64_'$DATE'.zip' manylinux2010_x86_64
zip -q -r '/Users/miklesz/Dysk Google/Demo/build/win_amd64_'$DATE'.zip' win_amd64
