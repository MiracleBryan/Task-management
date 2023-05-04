#!/bin/bash

# You will need nodejs, npm, quasar-cli, python3 and pip installed.

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
rm -rf BUILD
mkdir BUILD
cp run.py app.py config.py BUILD
cp -r utility database api BUILD
mkdir BUILD/frontend/
cp -r frontend/dist BUILD/frontend/

echo "Build located at the BUILD folder"
echo "Build Complete!"