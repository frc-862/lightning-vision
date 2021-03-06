# Lightning Vision Codebase

[![TensorFlow 2.5](https://img.shields.io/badge/TensorFlow-2.5-FF6F00?logo=tensorflow)](https://github.com/tensorflow/tensorflow/releases/tag/v2.5.0)
[![Python 3.6](https://img.shields.io/badge/Python-3.6-3776AB)](https://www.python.org/downloads/release/python-360/)
[![JetPack Version](https://badges.fyi/static/JetPack/4.6/green)](https://developer.nvidia.com/embedded/jetpack)\
[![Release](https://github.com/frc-862/tfod-wkspc/actions/workflows/release.yml/badge.svg)](http://hub.docker.com/r/edurs0/tfod-wkspc)
[![Docs](https://readthedocs.org/projects/pip/badge/)](https://github.com/frc-862/tfod-wkspc/blob/master/docs)

Base computer vision program for team 862's robots.\
Configured to run on a [NVIDIA Jetson Nano 2gb](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-nano/education-projects/).

This project is also intended to provide an easy-to-use environment where object detection models can be trained using the [TensorFlow Object Detection API](https://github.com/tensorflow/models/blob/master/research/object_detection/README.md).\
The [TensorFlow Object Detection API](https://github.com/tensorflow/models/blob/master/research/object_detection/README.md) comes installed in the provided [docker images](http://hub.docker.com/r/edurs0/tfod-wkspc).\
The Jetson image is based on the [NVIDIA l4t-tensorflow image](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/l4t-tensorflow)
and the other images are based on the [base tensorflow image](https://hub.docker.com/r/tensorflow/tensorflow).

**Contents:**\
[Here](#installation) are instructions for installing tools needed to work with this project.\
[Here](#usage) are instructions for working with the docker image.\
[Here](https://github.com/frc-862/tfod-wkspc/blob/master/docs/TRAINING.md) are instructions for training a custom object detection model.\
[Here](https://github.com/frc-862/tfod-wkspc/blob/master/docs/INFERENCE.md) are instructions for running inference on a trained model with OpenCV & TensorFlow.

## Installation

### Jetson Nano 2gb

To setup a [NVIDIA Jetson Nano 2gb](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-nano/education-projects/), follow [this setup guide](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-2gb-devkit#intro) to image an SD card, and boot up the Jetson.\
Note that [this user guide](https://developer.nvidia.com/embedded/learn/jetson-nano-2gb-devkit-user-guide) is also a great resource.

Once you have setup the Jetson, you will need to connect to internet.\
Be sure the USB WiFi Card is plugged in.\
This can be done by running the following command:

```bash
sudo nmcli device wifi connect <ssid> password <password>
```

Alternatively, if you need to connect to a hidden network, run the following commands (from [this post](https://stackoverflow.com/questions/35476428/how-to-connect-to-hidden-wifi-network-using-nmcli)):

```bash
sudo nmcli c add type wifi con-name <connect name> ifname wlan0 ssid <ssid>
sudo nmcli con modify <connect name> wifi-sec.key-mgmt wpa-psk
sudo nmcli con modify <connect name> wifi-sec.psk <password>
sudo nmcli con up <connect name>
```

Install cscore and other dependencies with

```bash
bash <(wget -qO- https://raw.githubusercontent.com/frc-862/lightning-vision/master/setup/setup.sh)
```

### All Devices

Now you are ready to fork & clone (or just clone, or just download) this repository.

```bash
# ssh
git clone git@github.com:frc-862/lightning-vision.git /tensorflow/workspace
# or https
git clone https://github.com/frc-862/lightning-vision.git /tensorflow/workspace
# or gh cli
gh repo clone frc-862/lightning-vision /tensorflow/workspace
```

Also install `labelImg` to label datasets.

```bash
pip3 install labelImg
```

Thats it!\
Now, you can begin [training](https://github.com/frc-862/lightning-vision/blob/master/docs/TRAINING.md) object detection models with tensorflow.

## Usage

The `Makefile` is the quickest way to work with the docker container.\
On your machine, simply run `sudo make <command> device=<device>`, where

`<device>` is either

- `jetson`
- `onboard`
- `cpu`
- `gpu`
- if no flag is specified, the deployment jetson container will be implied

and `<command>` is any of the following:

- `onboard` runs the container on a robot.\
This should only be used on a robot.
- `qemu` sets up the local docker environment to be able to build for arm64 processors.\
This should be used when you are building the image on a machine of a different arch.
- `run` will run the docker container on the machine.\
Use this command directly on the jetson.
- `resume` will restart the container if it has been stopped.
- `clean` will delete a stopped container.
- `shell` will shell into an active container/
- `purge` will remove the image from the local docker registry.
- `build` will create the docker image.
- `deploy` will build the image and push it to the hub.
- `push` will push the image to the hub.
- `pull` will pull the image from the hub.

### Building the Image

In the root directory of the project, run:

```bash
sudo make build
```

#### Soultions to Possible Issues Building the Image

1. On Windows, install [this make](http://gnuwin32.sourceforge.net/packages/make.htm) and add it to your path.
2. If you get some error such as\
`Opening zip "/proc/self/exe": lseek(): Bad file descriptor`\
when docker is building a python package, run\
`sudo make qemu`\
and try again.

#### Automated Builds on GitHub Actions

GitHub Actions is configured to build the images on all PRs and release the images on all pushes to `master`.

### Other Known Issues

- [This issue with tensor shape during training on Jetson/Other Devices](https://github.com/tensorflow/models/issues/9133).
  - Training works fine in notebooks on [colab](https://colab.research.google.com/).
- CPU & GPU images can only run on amd64 processors (tensorflow base image not available for arm64).
