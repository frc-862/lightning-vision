#!/bin/zsh

sudo systemctl unmask docker
sudo service docker start
sudo service docker status
docker run -d \
    --rm \
    -p 8080:8080 \
    --name "tfod-test" \
    --env AUTHENTICATE_VIA_JUPYTER="root" \
    edurs0/tfod-wkspc

