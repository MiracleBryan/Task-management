#!/bin/bash

echo "Installing system requirements"
sudo apt update
sudo apt -y upgrade
sudo apt install -y curl

# Backend - System
sudo apt -y install python3
sudo apt -y install python3-pip

# Frontend - System
# Update NodeJS
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt -y install nodejs
sudo apt -y install npm
# Quasar CLI
sudo npm i -g @quasar/cli

# Environment Variables
ENV="PRODUCTION"

echo "Building app for deployment.. $ENV"

echo "Building Flask.."
echo "Installing python requirements"
pip install -r requirements.txt

echo "Building Vue.."
cd frontend
npm install
quasar build

echo "Finalizing build.."
cd ..
sudo rm -rf BUILD
mkdir BUILD
cp run.py app.py config.py BUILD
cp -r utility database api BUILD
mkdir BUILD/frontend/
cp -r frontend/dist BUILD/frontend/

echo "Build located at the BUILD folder"
echo "Build Complete!"