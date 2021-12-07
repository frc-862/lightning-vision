# Define Variables
IMAGE_DIRECTORY="/tensorflow/workspace/power-port-targeting"
RATIO=0.1
SCRIPTS="/tensorflow/workspace/scripts"

# Run Partition Script
python3 $SCRIPTS/preprocessing/partition-dataset.py \
    -i $IMAGE_DIRECTORY \
    -r $RATIO \
    -x
