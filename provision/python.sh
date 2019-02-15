#!/usr/bin/env bash

apt-get update
apt-get install -y python 3.5.2
apt-get install -y python3-pip
apt-get install -y git
apt-get install -y libxml2
pip3 install -U
pip3 install asyncio
pip3 install discord
pip3 install urllib
pip3 install pyquery

cd /vagrant
git pull
python3 main.py