#! /bin/bash

# to run
xhost local:root
docker run -ti --rm \
  -e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v $HOME/.Xauthority:/home/feelpp/.Xauthority \
   --env QT_X11_NO_MITSHM=1 \
   -v /opt/DISTENE/DLim:/opt/DISTENE/DLim \
   -v /home/LNCMI-G/trophime/feelpp/research/hifimagnet/projects/HL-31:/home/feelpp/data \
  --net=host --pid=host --ipc=host \
  feelpp/salome:8.4.0-nvidia

