#!/bin/bash

echo "Updating LUbuntu System"
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update
sudo apt -y upgrade
sudo apt install -y curl

# Install Screen
sudo apt -y install screen

# Backend - System
# Install Python 3.11
echo "Installing Python Version 3.11"
sudo apt -y install python3.11
sudo apt -y install python3-pip

# Upgrade PIP
echo "Upgrading pip"
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# Frontend - System
# Update NodeJS
echo "Installing NodeJS"
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt -y install nodejs
sudo apt -y install npm
# Quasar CLI
sudo npm install -g @quasar/cli

# Install Requirements
echo "Flask - BackEnd - Installing python requirements.."
python3.11 -m pip install -r requirements.txt

echo "Vue - FrontEnd - Installing node packages.."
cd frontend
npm install