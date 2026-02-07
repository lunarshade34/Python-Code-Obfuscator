@echo off
echo Install Packages...
echo ======================================

python -m pip install --upgrade pip

python -m pip install --upgrade argparse base64 marshal zlib pathlib

echo.
echo Install Success!
pause