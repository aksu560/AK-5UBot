#!/usr/bin/env bash
sudo apt update
sudo apt -y install python3-pip
sudo apt -y install python-Levenshtein
pip3 install discord
pip3 install pyquery
pip3 install markovify
pip3 install fuzzywuzzy
pip3 install configparser
pip3 install praw
pip3 install chatterbot
pip3 install chatterbot_corpus

cd /vagrant
nohup python3 main.py &