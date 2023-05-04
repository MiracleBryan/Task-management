#!/bin/bash

# Run BackEnd Development.
echo "Starting Backend.."
screen -S task_management_app_backend -d -m python3.11 run.py

# Run FrontEnd.
cd frontend
echo "Starting Frontend.."
screen -S task_management_app_frontend -d -m quasar dev

echo ""
echo "      URL       |                     Description"
echo "localhost:5000  | Backend  : Swagger API documentation for backend development."
echo "localhost:8080  | Frontend : Application development."

# Note:
# Python runs the Flask server on development port 5000.
# Quasar runs the Frontend developement server at port 8080.
# Because this is for marking / assessment in LUbuntu, we will use these ports.
# In the deployed AWS application, port 80 and 443 will be used.

# URLs:
# localhost:5000 will bring you to the Swagger API documentation for our backend development.
# localhost:8080 will bring you to our frontend application.