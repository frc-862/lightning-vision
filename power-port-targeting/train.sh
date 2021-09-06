# Define Variables
WORKSPACE="/tensorflow/workspace/power-port-targeting"
DETECTOR_HOME="/tensorflow/models/research/object_detection"
MODEL_TYPE="ssd_mobilenet_v2_keras"

# Run Training Job
python $DETECTOR_HOME/model_main_tf2.py \
    --model_dir=models/$MODEL_TYPE \
    --pipeline_config_path=models/$MODEL_TYPE/pipeline.config \
    --checkpoint_dir=models/$MODEL_TYPE/ \
    --eval_dir=models/$MODEL_TYPE/

# To View Training Progress run
# tensorboard --logdir=$WORKSPACE/models/$MODEL_TYPE

# Export Trained Model
python $DETECTOR_HOME/exporter_main_v2.py \
    --input_type image_tensor \
    --pipeline_config_path $WORKSPACE/models/$MODEL_TYPE/pipeline.config \
    --trained_checkpoint_dir $WORKSPACE/models/$MODEL_TYPE/ \
    --output_directory $WORKSPACE/exported-models/trained_$MODEL_TYPE
