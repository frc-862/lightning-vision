#!/bin/bash
# Usage: ./deploy.sh [remote username] [remote ip]
rsync -zravP --delete ./voidvision/ ${1}@${2}:/home/${1}/voidvision/