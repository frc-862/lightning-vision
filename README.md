# TensorFlow Object Detection Workspace

[![TensorFlow 2.5](https://img.shields.io/badge/TensorFlow-2.5-FF6F00?logo=tensorflow)](https://github.com/tensorflow/tensorflow/releases/tag/v2.5.0)
[![Python 3.6](https://img.shields.io/badge/Python-3.6-3776AB)](https://www.python.org/downloads/release/python-360/)
[![Docker CPU Image](https://badges.fyi/static/Docker/CPU/blue)](http://hub.docker.com/r/edurs0/tfod-wkspc)
[![Docker GPU Image](https://badges.fyi/static/Docker/GPU/blue)](http://hub.docker.com/r/edurs0/tfod-wkspc)
[![Docs](https://readthedocs.org/projects/pip/badge/)](https://github.com/edurso/tfod-wkspc/blob/master/docs)

[![Build CPU Image](https://github.com/edurso/tfod-wkspc/actions/workflows/build-cpu.yml/badge.svg)](http://hub.docker.com/r/edurs0/tfod-wkspc)
[![Build GPU Image](https://github.com/edurso/tfod-wkspc/actions/workflows/build-gpu.yml/badge.svg)](http://hub.docker.com/r/edurs0/tfod-wkspc)

Disclaimer: Nothing here really works yet.

This project is intended to provide an easy-to-use environment where object detection models can be trained using the [TensorFlow Object Detection API](https://github.com/tensorflow/models/blob/master/research/object_detection/README.md).\
The [TensorFlow Object Detection API](https://github.com/tensorflow/models/blob/master/research/object_detection/README.md) comes installed in the two provided docker images.

[Here](#installation) are instructions for installing tools needed to work with this project.\
[Here](#building) are instructions for manually building the docker images.\
[Here](https://github.com/edurso/tfod-wkspc/blob/master/docs/TRAINING.md) are instructions for training a custom object detection model.\
[Here](https://github.com/edurso/tfod-wkspc/blob/master/docs/INFERENCE.md) are instructions for running inference on a trained model with OpenCV & TensorFlow.\
[Here](https://github.com/edurso/tfod-wkspc/blob/master/docs/JETSON-NANO.md) are instructions for setting up a NVIDIA Jetson Nano (2GB) as a developmen environment for this project.

## Installation

Install [Docker](https://docs.docker.com/get-docker/) on your respective os.

It would also be a good idea to install [Python](https://www.python.org/downloads/).

After installing python, you will need to install `labelImg` in order to label datasets.

```python
pip install labelImg
```

You will then need to fork & clone (or just clone) this repository.

```bash
# ssh
git clone git@github.com:edurso/tfod-wkspc.git
# or https
git clone https://github.com/edurso/tfod-wkspc.git
# or gh cli
gh repo clone edurso/tfod-wkspc
```

Everything else needed to work with the [TensorFlow Object Detection API](https://github.com/tensorflow/models/blob/master/research/object_detection/README.md) will be in the [Docker Image](http://hub.docker.com/r/edurs0/tfod-wkspc).
There is a separate [Docker Image](http://hub.docker.com/r/edurs0/tfod-wkspc-gpu) for machines with GPUs.

## Building

Use the respective `build.sh` scripts in the `cpu/` or `gpu/` subdirectories.\
Both the CPU and GPU docker images are* compatable with amd64 or arm64 processor architectures.

*CPU image is, but the [GitHub Actions](#github-actions) gpu build keeps failing due to limited drive space, so it is only arm64 compatible now.\
You will have to build for amd64 systems.

When it fails due to a [bazel](https://bazel.build/) related error on a python package installation step, such as below:

```sh
#17 0.467 Opening zip "/proc/self/exe": lseek(): Bad file descriptor
#17 0.473 [FATAL 22:55:57.506 src/main/cpp/archive_utils.cc:51] Failed to open '/proc/self/exe' as a zip file: (error: 9): Bad file descriptor
```

Run this container to fix the docker environment:

```bash
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
```

### GitHub Actions

GitHub Actions is configured to build and push both containers when pushed to the `build` branch.
