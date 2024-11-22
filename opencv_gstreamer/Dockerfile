FROM ubuntu:20.04
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y tzdata && \
    echo "America/Sao_Paulo" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata
ENV DEBIAN_FRONTEND=dialog

# Configurar o Python 3.9 já instalado
RUN ln -sf /usr/bin/python3.9 /usr/bin/python && \
    ln -sf /usr/bin/python3.9 /usr/bin/python3

RUN apt-get update && apt-get install --no-install-recommends -y \
    apt-utils \
    build-essential \
    curl

RUN apt-get install --no-install-recommends -y \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-good \
    gstreamer1.0-x \
    gstreamer1.0-libav \
    gstreamer1.0-tools

RUN apt-get install --no-install-recommends -y \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    libglib2.0-dev
RUN apt-get install --no-install-recommends -y wget ca-certificates

# Instalar dependências para suporte ao GTK
RUN apt-get update && apt-get install -y \
    libgtk2.0-dev \
    libgtk-3-dev \
    pkg-config

# Baixar e instalar o Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    bash /tmp/miniconda.sh -b -p /root/miniconda3 && \
    rm /tmp/miniconda.sh && \
    /root/miniconda3/bin/conda init bash

# Atualizar o Conda e instalar Python 3.9 com pacotes necessários
RUN /root/miniconda3/bin/conda update -n base -c defaults conda -y && \
    /root/miniconda3/bin/conda install python=3.9 jupyterlab notebook -c conda-forge -y

WORKDIR /notebooks

RUN apt install -y git cmake
COPY install_opencv_with_gstreamer.sh /notebooks/
RUN ./install_opencv_with_gstreamer.sh

# Adicionar as instruções extras após o script
# 1. Instalar pycairo
RUN apt-get update && apt-get install -y libcairo2 libcairo2-dev
RUN pip install pycairo

# 2. Instalar PyGObject
RUN apt-get update && apt-get install -y \
    libcairo2-dev \
    libgirepository1.0-dev \
    gobject-introspection \
    gir1.2-gtk-3.0 \
    pkg-config \
    build-essential
RUN pip install PyGObject

# 3. Instalar gcc-11 e configurar libstdc++
RUN apt-get update && apt-get install -y software-properties-common && \
    add-apt-repository ppa:ubuntu-toolchain-r/test && \
    apt-get update && \
    apt-get install -y gcc-11 g++-11 libstdc++-11-dev && \
    ln -sf /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.32 /usr/lib/x86_64-linux-gnu/libstdc++.so.6

# 4. Resolver problema do libffi com libgobject
RUN apt-get update && apt-get install -y libffi-dev libffi7 libgirepository1.0-dev && \
    cp /usr/lib/x86_64-linux-gnu/libffi.so.7 /root/miniconda3/lib/ && \
    ln -sf /root/miniconda3/lib/libffi.so.7 /root/miniconda3/lib/libffi.so.6

# Adicionar pacotes Python
RUN pip install annotated-types attrs future lxml numpy pillow pyarrow \
    pydantic pydantic_core pymavlink rerun-sdk scipy typing_extensions

CMD ["/root/miniconda3/bin/jupyter","notebook", "--allow-root"]

