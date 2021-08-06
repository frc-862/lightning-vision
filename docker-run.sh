#!/bin/zsh

sudo systemctl unmask docker
sudo service docker start
sudo service docker status
docker run --rm --name tfod-test -it -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY edurs0/tfod bash

