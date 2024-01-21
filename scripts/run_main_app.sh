#!/bin/bash
python_path="/home/pi/projects/boat/boat-monitor/venv/bin/python"
main_app="/home/pi/projects/boat/boat-monitor/boat_app/boat_app_lite.py --main_app"
session_name="boat_app"

# Kill the session if it already exists
if tmux has-session -t "$session_name" 2>/dev/null; then
    # If the session exists, kill it
    #tmux kill-session -t "$session_name"
    #echo "old tmux session '$session_name' killed."
    echo "tmux session '$session_name' is running."
else
    # If the session does not exist, display a message
    echo "tmux session '$session_name' not found."
    tmux new-session -d -s boat_app "${python_path} ${main_app}"
    echo "new tmux session '$session_name' started."
fi
