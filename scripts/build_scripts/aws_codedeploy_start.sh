#!/bin/bash

echo "Starting Application"
cd /task_management_app

# Uses Screen to run backend in background.
# To list all active screens (Note, Remember to sudo!): [sudo screen -ls]
# To terminate: [sudo screen -X -S task_management_app_session quit]
# To start: [sudo screen -S task_management_app_session -d -m sudo ENV=PRODUCTION python3 /task_management_app/run.py]
screen -S task_management_app_session -d -m sudo ENV=PRODUCTION python3 run.py