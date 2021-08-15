#!/bin/zsh

image="edurs0/tfod-wkspc"

echo "Run gpu container (y/n)?"
read gpu
if [[ $gpu == "y" ]]; then
    image="edurs0/tfod-wkspc-gpu"
fi

docker run --rm --name tfod -it -p 8888:8888 $image

