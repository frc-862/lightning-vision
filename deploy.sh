#!/bin/sh
# Usage: ./deploy.sh [remote username] [remote ip]
if [ -z "$1" ] || [ -z "$2" ] ; then
    echo "No command line arguments given"
    echo "Defaulting connection to lightning@10.8.62.10"
    rsync -zravP --delete ./voidvision/ lightning@10.8.62.10:/home/lightning/voidvision/
else
    echo "Connecting to $1 at $2"
    rsync -zravP --delete ./voidvision/ ${1}@${2}:/home/${1}/voidvision/
fi
