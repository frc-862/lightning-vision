#!/bin/zsh

IMAGE="edurs0/tfod-wkspc"

PATH="//d/workspace/tfod-wkspc"

echo "enter absolute path to workspace"
read WORKSPACE

if [ -d "$WORKSPACE" ]; then
    PATH=WORKSPACE
fi

echo "run gpu container (y/n)?"
read GPU
if [[ $GPU == "y" ]]; then
    IMAGE="edurs0/tfod-wkspc-gpu"
fi

docker run --rm --name tfod -it -p 8888:8888 -v $PATH:/tensorflow/workspace $IMAGE

