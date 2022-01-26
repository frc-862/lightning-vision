#!/bin/sh
echo "Waiting 5 seconds..."
sleep 5
export PYTHONUNBUFFERED=1
python3 /app/voidvision/cameraserver.py
