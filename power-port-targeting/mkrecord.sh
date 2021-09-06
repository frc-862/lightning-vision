# Define Variables
WORKSPACE="/tensorflow/workspace/power-port-targeting"
SCRIPTS="/tensorflow/workspace/scripts"

# Generate TFRecord for Training Data
python $SCRIPTS/preprocessing/generate-tfrecord.py \
    -x $WORKSPACE/images/train \
    -l $WORKSPACE/annotations/label-map.pbtxt \
    -o $WORKSPACE/annotations/train.record

# Generate TFRecord for Validation Data
python $SCRIPTS/preprocessing/generate-tfrecord.py \
    -x $WORKSPACE/images/test \
    -l $WORKSPACE/annotations/label-map.pbtxt \
    -o $WORKSPACE/annotations/test.record
