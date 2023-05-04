#!/bin/bash

# Quits FrontEnd and BackEnd Sessions.
echo "Quitting frontend and backend server sessions.."
screen -XS task_management_app_backend quit
screen -XS task_management_app_frontend quit