#!/bin/zsh

# Define Variables
#FILEPATH="//d/workspace/tfod-wkspc"
FILEPATH="/mnt/d/workspace/tfod-wkspc"
IMAGE="edurs0/tfod-wkspc"

# Determine if we Need to Run the GPU Container
echo "run gpu container (y/n)?"
read GPU
if [[ $GPU == "y" ]]; then
    IMAGE="edurs0/tfod-wkspc-gpu"
fi

# Start Docker
docker run \
    --rm \
    --name tfod \
    -it \
    -p 8888:8888 \
    -p 6006:6006 \
    -v $FILEPATH:/tensorflow/workspace \
    $IMAGE

