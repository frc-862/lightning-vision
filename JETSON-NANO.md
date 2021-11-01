# Jetson Nano 2gb

![nVIDIA](https://img.shields.io/badge/nVIDIA-%2376B900.svg?style=for-the-badge&logo=nVIDIA&logoColor=white)

The following instructions go over how to setup the [Jetson Nano 2gb](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-nano/education-projects/) for this project.

It will go over how to set it up as both a development environment and a functional end-product.

## Development Environment

First, walk through [this setup guide](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-2gb-devkit#intro) to image an SD card, and boot up the Jetson.\
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

At this point, feel free to customize the installation of Debian to suit your preferences.

Now, you can clone this repository and follow the instructions in the README to train a model.

## Deployment

I still need to figure this out.
