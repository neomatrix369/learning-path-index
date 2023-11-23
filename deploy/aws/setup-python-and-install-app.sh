#!/bin/bash

set -eu
set -o pipefail

sudo apt-get update
sudo apt-get install -y python3-pip
pip3 --version
python --version

git clone https://github.com/neomatrix369/learning-path-index
#cd learning-path-index
#pip install -r requirements.txt