# Maze control for behavioural rat training

![maze](models3d/maze.png)

# Installation


## Raspberry pi 3

Mazer-Service

run install.sh with sudo or run the following commands

cd rat-maze/mazer-service
cp mazer-service.py /usr/bin
cp mazer.service /lib/systemd/system/
systemctl deamon-reload
systemctl enable mazer.service
reboot


Package needed 
numpy # for random numbers

