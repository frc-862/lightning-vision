#!/bin/zsh

# Define Constants
WORKSPACE="/tensorflow/workspace"

# Placeholders
unset NAME

# Function Displays The "Help" Function for This Script
usage() {
    echo "usage: new.sh -n <NAME>"
    echo "    -n NAME the name of project to create"
}

# Help Function - Directcts To `usage`
help() {
    echo "use '-h' for more information"
    exit 1
}

# Get Input From Flags With Script
while getopts "n:h" flag; do
    case $flag in
        n)       NAME=$OPTARG ;;
        h)       help
                 exit 1 ;;
        \?)      usage
                 exit 2 ;;
    esac
done
shift `expr $OPTIND - 1`


# Check NAME Flag Input Valid
if [ -z "$NAME" ]; then
    echo "fatal: missing path to workspace"
    echo "try running again with '-n NAME'"
    help
fi

# Make Directory Structure
mkdir -p $WORKSPACE/$NAME/annotations
touch $WORKSPACE/$NAME/annotations/label-map.pbtxt
mkdir -p $WORKSPACE/$NAME/exported-models
touch $WORKSPACE/$NAME/exported-models/.gitkeep
mkdir -p $WORKSPACE/$NAME/images/train
touch $WORKSPACE/$NAME/images/train/.gitkeep
mkdir -p $WORKSPACE/$NAME/images/test
touch $WORKSPACE/$NAME/images/test/.gitkeep
mkdir -p $WORKSPACE/$NAME/models
touch $WORKSPACE/$NAME/models/.gitkeep
mkdir -p $WORKSPACE/$NAME/pre-trained-models
touch $WORKSPACE/$NAME/pre-trained-models/.gitkeep

