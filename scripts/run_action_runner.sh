#!/bin/bash
action_runner="/home/pi/projects/boat/actions-runner/run.sh"
session_name="action_runner"

# Kill the session if it already exists
if tmux has-session -t "$session_name" 2>/dev/null; then
    # If the session exists, kill it
    #tmux kill-session -t "$session_name"
    #echo "old tmux session '$session_name' killed."
    # Don't kill it.
    echo "tmux session '$session_name' is running."
else
    # If the session does not exist, display a message
    echo "tmux session '$session_name' not found."
    tmux new-session -d -s action_runner "/home/pi/projects/boat/actions-runner/run.sh"
    tmux ls
    echo "new tmux session '$session_name' started."
fi
