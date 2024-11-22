According to: https://github.com/Dorozhko-Anton/ComputerVisionStreams/tree/main/Opencv%2BGstreamer

# Step to run the docker
docker build -t gstreamer:base .

export DISPLAY=:0

xhost +

docker run -it --rm --net=host --gpus all -e DISPLAY=$DISPLAY -p 8888:8888 --device /dev/snd -v /tmp/.X11-unix/:/tmp/.X11-unix -v $PWD:/notebooks/ gstreamer:base
__________
Esta parte deve dar erro em: --gpus all
Essa flag pode ser tirada caso não necessite de suporte para GPU

# Outra opção é usar este comando:

docker exec -it $(docker ps -q -f ancestor=gstreamer:base) /bin/bash

Ou este sugerido pelo chat gpt:

docker run -it --net=host -e DISPLAY=$DISPLAY -p 8888:8888 --device /dev/snd -v /tmp/.X11-unix/:/tmp/.X11-unix -v $PWD:/notebooks/ gstreamer:base


docker run -it -v /home/alysson/bluerov2-TCC/codes:/codes gstreamer:base

