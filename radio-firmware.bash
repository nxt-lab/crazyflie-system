#!/bin/sh
cd ~/crazyflie/crazyflie_ws/src/crazyradio-firmware/firmware
sudo python ../usbtools/launchBootloader.py
sudo python ../usbtools/nrfbootload.py flash bin/cradio-pa-0.53.bin
printf "Unplug now...\n"
read _
lsusb -d 1915:7777 -v | grep bcdDevice
