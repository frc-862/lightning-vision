#!/bin/sh
# Usage: ./deploy.sh [remote username] [remote ip]

# NOTE: Since we use absolute paths we must put voidvision in /home/lightning to have things run properly on startup
# TODO: Once current testing Jetson is reimaged to have lightning be default user remove remote username arg
if [ -z "$1" ] || [ -z "$2" ] ; then
    echo "No command line arguments given"
    echo "Defaulting connection to lightning@10.8.62.3"
    rsync -zravP ./voidvision/ lightning@10.8.62.3:/home/lightning/voidvision/
else
    echo "Connecting to $1 at $2"
    rsync -zravP ./voidvision/ ${1}@${2}:/home/lightning/voidvision/
fi
