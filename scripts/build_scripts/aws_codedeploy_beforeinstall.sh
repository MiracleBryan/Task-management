#!/bin/bash

echo "Before Install"

# Kill screen previous sessions and restart.
screen -XS task_management_app_session quit
pkill screen

# Delete old version.
rm -rf /task_management_app