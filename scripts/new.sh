# Define Variables
WORKSPACE="/tensorflow/workspace"
NAME='power-port-targeting'

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
