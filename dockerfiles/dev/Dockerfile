FROM nvcr.io/nvidia/l4t-tensorflow:r32.6.1-tf2.5-py3

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Detroit

RUN apt-get update \
    && apt-get install -y \
    python3.6 \
    python3-pip \
    python3-lxml \
    wget \
    && python3 -m pip install --upgrade pip

RUN wget https://github.com/tensorflow/io/archive/refs/tags/v0.19.1.tar.gz \
    && tar -xvzf v0.19.1.tar.gz && cd io-0.19.1/ \
    && chmod +x ./configure.sh \
    && ./configure.sh \
    && python3 setup.py -q bdist_wheel --project tensorflow_io_gcs_filesystem \
    && cd dist && pip3 install $(ls | grep *.whl) \
    && cd .. && pip3 install . \
    && cd .. && rm -rf io-0.19.1.tar.gz io-0.19.1/

RUN pip3 install \
    numpy==1.19.5 \
    numba==0.53.1 \
    pandas==1.1.5 \
    scipy==1.5.4 \
    scikit-learn==0.23.2 \
    jupyterlab==2.2.9 \
    matplotlib==3.3.4 
