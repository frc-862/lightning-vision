FROM "ubuntu:bionic"

RUN apt-get update && yes | apt-get upgrade

RUN mkdir -p /tensorflow/models

RUN apt-get install -y python3
RUN apt-get install -y git python3-pip

RUN pip3 install --upgrade pip

RUN pip3 install tensorflow==2.2.0

RUN apt-get install -y protobuf-compiler python3-pil python3-lxml
RUN pip3 install jupyter
RUN pip3 install matplotlib
RUN pip3 install tf_slim
RUN pip3 install pycocotools
RUN pip3 install labelImg

RUN git clone https://github.com/tensorflow/models.git /tensorflow/models

WORKDIR /tensorflow/models/research

RUN cp object_detection/packages/tf2/setup.py .
RUN python3 -m pip install .

RUN protoc object_detection/protos/*.proto --python_out=.

RUN export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim

#RUN jupyter notebook --generate-config --allow-root

#RUN echo "c.NotebookApp.password = u'sha1:6a3f528eec40:6e896b6e4828f525a6e20e5411cd1c8075d68619'" >> /root/.jupyter/jupyter_notebook_config.py

#EXPOSE 8888

#CMD ["jupyter", "notebook", "--allow-root", "--notebook-dir=/tensorflow/models/research/object_detection", "--ip=0.0.0.0", "--port=8888", "--no-browser"]

