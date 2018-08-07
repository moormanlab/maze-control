#!/bin/sh
cp mazer-service.py /usr/bin
cp mazer.service /lib/systemd/system/
systemctl deamon-reload
systemctl enable mazer.service
reboot
