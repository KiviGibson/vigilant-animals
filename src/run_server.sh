#!bin/bash
watchmedo auto_restart -- "*.py" --recursive --signal SIGTERM \ python server.py
