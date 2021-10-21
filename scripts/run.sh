#!/bin/zsh

# Define Variables
CPU_IMAGE="edurs0/tfod-wkspc"
GPU_IMAGE="edurs0/tfod-wkspc-gpu"

# Placeholders
unset IMAGE
unset FILEPATH
unset NAME

# Function Displays The "Help" Function for This Script
usage() {
    echo "usage: ./run.sh -f <FILEPATH> -(c|g) -n <NAME>? -h?"
    echo "    -f FILEPATH the path to the workspace"
    echo "    -g use this tag if you have a TF2.x compatible GPU"
    echo "    -c use this tag if you only have a CPU"
    echo "    -n NAME (optional) the name of the docker image to start"
    echo "    -h (optional) displays this message"
}

# Help Function - Directcts To `usage`
help() {
    echo "use '-h' for more information"
    exit 1
}

# Set Default Image to CPU Image
IMAGE=$CPU_IMAGE

# Get Input From Flags With Script
while getopts "gcf:hn:" flag; do
    case $flag in
        g)       IMAGE=$GPU_IMAGE ;;
        c)       IMAGE=$CPU_IMAGE ;;
        f)       FILEPATH=$OPTARG ;;
        n)       NAME=$OPTARG ;;
        h)       usage
                 exit ;;
        \?)      usage
                 exit 2 ;;
    esac
done
shift `expr $OPTIND - 1`

# Check IMAGE Flag Input Valid
if [ -z "$IMAGE" ]; then
    echo "fatal: missing processer tag"
    echo "try running again with '-c' or '-g'"
    help
fi

# Check FILEPATH Flag Input Valid
if [ -z "$FILEPATH" ]; then
    echo "fatal: missing path to workspace"
    echo "try running again with '-f FILEPATH'"
    help
fi

# Check FILEPATH Is A Directory
if [ ! -d "$FILEPATH" ]; then
    echo "fatal: provided path does not exist"
    help
fi

# Check NAME Flag Input (Optional)
if [ -z "$NAME" ]; then
    NAME="tfod"
fi

# Start Docker
docker run \
    --rm \
    --name $NAME \
    -it \
    -p 8888:8888 \
    -p 6006:6006 \
    -v $FILEPATH:/tensorflow/workspace \
    $IMAGE

