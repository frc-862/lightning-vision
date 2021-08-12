#!/bin/zsh

sudo sudo systemctl unmask docker
sudo service docker start
sudo service docker status
docker build -t edurs0/tfod-wkspc-gpu ./gpu/

