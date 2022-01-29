#!/bin/sh
echo 'deb http://download.opensuse.org/repositories/home:/auscompgeek:/robotpy/Ubuntu_18.04_Ports/ /' | sudo tee /etc/apt/sources.list.d/home:auscompgeek:robotpy.list

apt install -y curl

curl -fsSL https://download.opensuse.org/repositories/home:auscompgeek:robotpy/Ubuntu_18.04_Ports/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/home_auscompgeek_robotpy.gpg > /dev/null

apt update

apt install python3-cscore
