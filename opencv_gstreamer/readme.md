According to: https://github.com/Dorozhko-Anton/ComputerVisionStreams/tree/main/Opencv%2BGstreamer

# Step to run the docker
docker build -t gstreamer:base .

export DISPLAY=:0

xhost +

docker run -it --rm --net=host --gpus all -e DISPLAY=$DISPLAY -p 8888:8888 --device /dev/snd -v /tmp/.X11-unix/:/tmp/.X11-unix -v $PWD:/notebooks/ gstreamer:base
_________________
Esta parte deve dar erro em: --gpus all
Essa flag pode ser tirada caso não necessite de suporte para GPU

# Outra opção é usar este comando:

**Abrir o container:** docker run -it --net=host -e DISPLAY=host.docker.internal:0 -p 8888:8888 -v /tmp/.X11-unix/:/tmp/.X11-unix -v "C:\Users\alyss\OneDrive\Documentos\TCC\pymavlink:/codes" gstreamer:base
(/codes vai apontar para a pasta que é descrita antes)

**Abrir o terminal do container em outro cmd:** docker exec -it cb3744aa38d8 /bin/bash

**Testar o pipeline:** gst-launch-1.0 udpsrc port=5600 ! application/x-rtp ! rtph264depay ! avdec_h264 ! videoconvert ! autovideosink

**Tentar esse:** gst-launch-1.0 udpsrc port=5600 caps='application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264' ! rtph264depay ! avdec_h264 ! queue ! autovideosink

**Instalar o VcXsrv** caso haja este erro: error: XDG_RUNTIME_DIR not set in the environment ou WARNING: from element /GstPipeline:pipeline0/GstAutoVideoSink:autovideosink0: Could not initialise Xv output
Additional debug info:
xvimagesink.c(1773): gst_xv_image_sink_open (): /GstXvImageSink:autovideosink0-actual-sink-xvimage:
Could not open display (null)

No linux para achar o id do container automaticamente: docker exec -it $(docker ps -q -f ancestor=gstreamer:base) /bin/bash

Ou este sugerido pelo chat gpt:

docker run -it --net=host -e DISPLAY=$DISPLAY -p 8888:8888 --device /dev/snd -v /tmp/.X11-unix/:/tmp/.X11-unix -v $PWD:/notebooks/ gstreamer:base
docker run -it -v /home/alysson/bluerov2-TCC/codes:/codes gstreamer:base

