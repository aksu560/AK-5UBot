#!/usr/bin/env bash

pip3 install lxml
pip3 install asyncio
pip3 install discord
pip3 install pyquery
pip3 install Pillow
pip3 install pytz
pip3 install fuzzywuzzy
pip3 install python-Levenshtein
pip3 install praw
pip3 install markovify
pip3 install selenium
pip3 install phantomjs-binary

wget -O /vagrant/Resources/Other/adblock.xpi https://addons.mozilla.org/firefox/downloads/latest/1865/addon-1865-latest.xpi

wget https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-linux64.tar.gz
tar -xvzf geckodriver*
chmod +x geckodriver
sudo mv geckodriver /usr/local/bin/

sudo apt install dnsutils