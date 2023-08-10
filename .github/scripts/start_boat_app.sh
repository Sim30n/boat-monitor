#!/bin/bash

# Define the session name
SESSION_NAME="boat-app"

# Kill the session if it already exists
tmux has-session -t $SESSION_NAME 2>/dev/null
if [ $? != 0 ]; then
    tmux kill-session -t $SESSION_NAME
fi

# Start a new tmux session with the defined name
tmux new-session -d -s $SESSION_NAME

# Send a command to the tmux session to start the Python program
tmux send-keys -t $SESSION_NAME "./home/pi/projects/boat/boat-monitor/venv/bin/python3 boat_app_lite.py" C-m

# Detach the tmux session
tmux detach-session -t $SESSION_NAME
