python generate-tfrecord.py \
    -x /tensorflow/workspace/power-port-targeting/images/train \
    -l /tensorflow/workspace/power-port-targeting/annotations/label-map.pbtxt \
    -o /tensorflow/workspace/power-port-targeting/annotations/train.record

python generate-tfrecord.py \
    -x /tensorflow/workspace/power-port-targeting/images/test \
    -l /tensorflow/workspace/power-port-targeting/annotations/label-map.pbtxt \
    -o /tensorflow/workspace/power-port-targeting/annotations/test.record

    