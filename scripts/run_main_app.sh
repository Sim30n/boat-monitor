#!/bin/bash
python_path="/home/pi/projects/boat/boat-monitor/venv/bin/python"
main_app="/home/pi/projects/boat/boat-monitor/boat_app/boat_app_lite.py --main_app"
tmux new-session -d -s boat_app "${python_path} ${main_app}"