# TensorFlow Workspace

[![TensorFlow 2.5](https://img.shields.io/badge/TensorFlow-2.5-FF6F00?logo=tensorflow)](https://github.com/tensorflow/tensorflow/releases/tag/v2.5.0)
[![Python 3.6](https://img.shields.io/badge/Python-3.6-3776AB)](https://www.python.org/downloads/release/python-360/)
[![Docker CPU Image](https://badges.fyi/static/Docker/CPU/blue)](http://hub.docker.com/r/edurs0/tfod-wkspc)
[![Docker GPU Image](https://badges.fyi/static/Docker/GPU/blue)](http://hub.docker.com/r/edurs0/tfod-wkspc-gpu)

[![Build CPU Image](https://github.com/edurso/tfod-wkspc/actions/workflows/build-cpu.yml/badge.svg)](http://hub.docker.com/r/edurs0/tfod-wkspc)
[![Build GPU Image](https://github.com/edurso/tfod-wkspc/actions/workflows/build-gpu.yml/badge.svg)](http://hub.docker.com/r/edurs0/tfod-wkspc-gpu)

Nothing here really works yet.

For instructions on how to get started, see [Installation](#installation), [Training](#training), and [Inference](#inference). See [Building](#building) for instructions on how to build the docker images.

## Building

Use the respective `build.sh` scripts in the `cpu/` or `gpu/` subdirectories.\
Both the CPU and GPU docker images are* compatable with amd64 or arm64 processor architectures.

*kinda but not yet really . . .

When it fails due to a [bazel](https://bazel.build/) related error on a python package installation step, such as below:

```sh
#17 0.467 Opening zip "/proc/self/exe": lseek(): Bad file descriptor
#17 0.473 [FATAL 22:55:57.506 src/main/cpp/archive_utils.cc:51] Failed to open '/proc/self/exe' as a zip file: (error: 9): Bad file descriptor
```

Run this container to fix the docker environment:

```bash
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
```

docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

## Installation

Install [Docker](https://docs.docker.com/get-docker/) on your respective os.

It would also be a good idea to install [Python](https://www.python.org/downloads/).

After installing python, you will need to install `labelImg` in order to label datasets.

```python
pip install labelImg
```

Everything else needed to work with the [TensorFlow Object Detection API](https://github.com/tensorflow/models/blob/master/research/object_detection/README.md) will be in the [Docker Image](http://hub.docker.com/r/edurs0/tfod-wkspc).
There is a separate [Docker Image](http://hub.docker.com/r/edurs0/tfod-wkspc-gpu) for machines with GPUs.

## Training

Below is an adapted version of [this](https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/index.html) tutorial on how to train custom models.

### Creating the Dataset

After putting the images in `images/`, run `labelImg images/` (from the project directory) and label the images.

At this point, we are ready to start our Docker container and finish set up there.

### Starting Docker Container

The `docker-run.sh` script will configure and run the docker container.
Before you run this script, change the `$FILEPATH` variable to the location of this project on your machine.
That directory will be mounted to `/tensorflow/workspace` in the container.
It is important to start the GPU container if you have a [compatable GPU](https://www.tensorflow.org/install/gpu).

The filesystem of the docker container is set up as follows:

```sh
/tensorflow/
├─ models/
│  ├─ community/
│  ├─ official/
│  ├─ orbit/
│  ├─ research/
│  └─ ...
└─ workspace/ (this repository)
   ├─ training-demo/ (and other projects)
   ├─ dockerfiles/
   │  ├─ cpu/
   │  │  ├─ Dockerfile
   │  │  └─ build.sh
   │  ├─ gpu/
   │  │  ├─ Dockerfile
   │  │  └─ build.sh
   │  └─ README.md
   ├─ scripts/
   │  ├─ preprocessing/
   │  │  └─ ...
   │  ├─ dataset-creation/
   │  │  └─ ...
   │  └─ ...
   ├─ docker-run.sh
   └─ README.md
```

Once the container starts, you will see that jupyter lab has started.
Go to one of the links the container has spat out (they all go to the same place) to see the jupyter environment.
Open a terminal from the launcher to continue.

### Setting Up Workspace

Create a directory structure like the one shown below in the root directory of this repository.
This will be the project directory.

```sh
training-demo/
├─ annotations/
├─ exported-models/
├─ images/
│  ├─ test/
│  └─ train/
├─ models/
└─ pre-trained-models/
```

Alternatively, you can simply run the `new.sh` script in the `scripts` directory to create a new workspace.

```sh
./scripts/new.sh -n training-demo
```

All `*.csv`, `*.pbtxt`, `*.record` and other similar files will be kept in `annotations/`.
These files describe the dataset. `exported-models` will house exported versions of trained models.
`images/` will store raw data files and their respective `*.xml` files.
Training data will be kept in `images/train/` and testing data will be kept in `images/test/`.
`models/` will contain a subdirectory for each training job, with the `pipeline.config` file and all of the files generated during training.
Raw, out-of-the-box, pre-trained models will be housed in `pre-trained-models/` and will be used as a starting checkpoint in each training job.

### Partitioning the Dataset

Now that the images are labeled, the dataset will need to be partitioned.
This can be done with the provided script `partition.sh` in `/tensorflow/workspace/scripts/`.
Before you run this script, be sure to set `$IMAGE_DIRECTORY` to the location of the image files and `$RATIO` to the percent of the image files, as a decimal, that should be used as validation data.
This script will not remove the files in `images/`, but will merely copy the images and their respective `*.xml` files to either the `images/train` or `images/test` directory.

### Create Label Map

Now that the dataset has been partitioned, we can creat a label map of the data.
Create a `label-map.pbtxt` file in the `annotations/` directory of the project.
Fill it with labels in the following format.
It is important to note that the `name` of each label much correspond to a value set in the `*.xml` file of an image.

```pbtxt
item {
    id: 1
    name: 'something'
}

item {
    id: 2
    name: 'something-else'
}
```

### Create TensorFlow Records

The `*.xml` format we have thus far is not usable with TensorFlow.
We need to convert the all the `*.xml` files to a single `*.record` file for both `images/test/` and `images/training/` in the project directory.
The `mkrecord.sh` script in `/tensorflow/workspace/scripts/` can do this for us.
Before running it, set `$WORKSPACE` to the project directory containing the `images/` subdirectory.

### Downloading Pre-Trained Model

Training a model from scratch is very difficult, and it is often better to start using a pre-trained model.
The process of re-training a trained model is called [Transfer Learning](https://en.wikipedia.org/wiki/Transfer_learning).

TensorFlow has a bunch of pre-trained models available in the [Model Zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md).

Pick one, download, and extract it into the `pre-trained-models/` subdirectory in the project directory.

If we were to use the [SSD ResNet 50 V1 FPN 640x640](http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_resnet50_v1_fpn_640x640_coco17_tpu-8.tar.gz) model, our project directory would look something like this:

```sh
training-demo/
├─ ...
├─ pre-trained-models/
│  └─ ssd_resnet50_v1_fpn_640x640_coco17_tpu-8/
│     ├─ checkpoint/
│     ├─ saved_model/
│     └─ pipeline.config
└─ ...
```

### Configuring the Training Model

Make a new directory under `models/` such as follows:

```sh
training-demo/
├─ ...
├─ models/
│  └─ my_ssd_resnet50_v1_fpn/
│     └─ pipeline.config
└─ ...
```

where `pipeline.config` is copied form the pre-trained model you downloaded.

Edit the following in the `pipeline.config` file:

- `model.ssd.num_classes`: set this to the number of different label classes as defined in `annotations/label-map.pbtxt`
- `train_config.batch_size`: set this to the desired batch size (larger batch sizes require more memory during training)
- `train_input_reader.label_map_path: "annotations/label-map.pbtxt"`
- `train_input_reader.tf_record_input_reader.input_path: "annotations/train.record"`
- `eval_config.metrics_set: "coco_detection_metrics"`: optional
- `eval_config.use_moving_averages: false`: optional
- `eval_input_reader.label_map_path: "annotations/label-map.pbtxt"`
- `eval_input_reader.tf_record_input_reader.input_path: "annotations/test.record"`

### Training and Exporting the Model

To train the model, you can use the `train.sh` script in `/tensorflow/workspace/scripts/`.
Before running `train.sh`, be sure to set `$WORKSPACE` to the project directory and `$MODEL_TYPE` to the model type, or the name of the directory housing the config in `models/` (idealy this will be the same as `model.feature_extractor.type` in the `pipeline.config`).

While the model is training, you can view its progress with [tensorboard](https://www.tensorflow.org/tensorboard) by running the finction below where `$WORKSPACE` and `$MODEL_TYPE` are the same as defined above.

```bash
tensorboard --logdir=$WORKSPACE/models/$MODEL_TYPE
```

After the model is trained and exported, you should see a new directory in `exported-models/` that houses the trained model.

The `*.pb` file for this model can be found in the `saved_model/` subdirectory. This model is ready to be depolyed to ... wherever.

## Inference

For inference with OpenCV, see [this sample implementation (python)](https://github.com/opencv/opencv/wiki/TensorFlow-Object-Detection-API).
