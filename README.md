# rat-maze
Maze control for behaviuoral rat training


Install on raspberry pi

Mazer-Service

run install.sh with sudo or run the following commands

cd rat-maze/mazer-service
cp mazer-service.py /usr/bin
cp mazer.service /lib/systemd/system/
systemctl deamon-reload
systemctl enable mazer.service
reboot
