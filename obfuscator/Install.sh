#!/bin/bash

echo "Install Packages..."
echo "======================================"

python3 -m pip install --upgrade pip

python3 -m pip install --upgrade argparse base64 marshal zlib

echo ""
echo "Install Success!"