#!/usr/bin/env bash
sudo apt install dnsutils
sudo apt install firefox
sudo apt-get install xvfb

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
pip3 install pyvirtualdisplay

wget -O /vagrant/Resources/Other/adblock.xpi https://addons.mozilla.org/firefox/downloads/latest/1865/addon-1865-latest.xpi

wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
tar -xvzf geckodriver*
chmod +x geckodriver*
sudo mv geckodriver /usr/local/bin/

wget http://ftp.mozilla.org/pub/firefox/releases/62.0.3/linux-$(uname -m)/en-US/firefox-62.0.3.tar.bz2
tar -xjf firefox-62.0.3.tar.bz2
sudo rm -rf /opt/firefox
sudo mv firefox /opt/firefox/
sudo mv /usr/bin/firefox /usr/bin/firefox_old
sudo ln -s /opt/firefox/firefox /usr/bin/firefox