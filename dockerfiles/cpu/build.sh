#!/bin/sh
# Build CPU Docker Image

# Placeholders
unset NEW_BUILDER

# Function Displays The "Help" Function for This Script
usage() {
    echo "usage: new.sh -n <NEW_BUILDER>?"
    echo "    -n NEW_BUILDER use this flag to indicate the use of a new builder with given name"
}

# Help Function - Directcts To `usage`
help() {
    echo "use '-h' for more information"
    exit 1
}

# Get Input From Flags With Script
while getopts "n:h" flag; do
    case $flag in
        n)       NEW_BUILDER=$OPTARG ;;
        h)       help
                 exit 1 ;;
        \?)      usage
                 exit 2 ;;
    esac
done
shift `expr $OPTIND - 1`

# Check NEW_BUILDER Flag Input Should Be Used
if [ -z "$NEW_BUILDER" ]; then
    docker buildx create --name $NEW_BUILDER
    docker buildx use $NEW_BUILDER
    docker buildx inspect --bootstrap
fi

docker buildx build --platform linux/amd64,linux/arm64 -t edurs0/tfod-wkspc:latest --push .


