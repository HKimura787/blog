FROM ubuntu:22.04

# OS環境を日本語ロケールに切り替える
ENV LANG ja_JP.UTF-8
ENV LC_ALL ja_JP.UTF-8
ENV TZ=Asia/Tokyo

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get dist-upgrade -y && \ 
    ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    apt-get clean

# 日本語フォントをインストールする
RUN apt-get update && \
    apt-get install -y fonts-ipaexfont fonts-noto-cjk && \
    apt-get clean

# Python3.10をインストールする
RUN apt-get install -y python3.10 python3.10-dev git && \ 
    apt-get clean
RUN apt-get install python3-pip -y && \
    apt-get clean
RUN apt-get install -y vim libgl1-mesa-dev libgtk2.0-dev && \
    apt-get clean

# jupyter関連
RUN python3.10 -m pip install --no-cache-dir \
            ipykernel \
            ipython \
            ipywidgets \
            jupyter
RUN jupyter notebook --generate-config
COPY jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py

# GUI関連 Xサーバーへの出力設定
RUN export DISPLAY=`hostname`.mshome.net:0.0

# Yoloの準備
RUN python3.10 -m pip install ultralytics
RUN git clone https://github.com/SkalskiP/yolov9.git
RUN python3.10 -m pip install -r yolov9/requirements.txt -q
RUN apt-get install wget -y && \
    apt-get clean
RUN wget -P yolov9/weights -q https://github.com/WongKinYiu/yolov9/releases/download/v0.1/yolov9-c.pt
RUN wget -P yolov9/weights -q https://github.com/WongKinYiu/yolov9/releases/download/v0.1/yolov9-e.pt
RUN wget -P yolov9/weights -q https://github.com/WongKinYiu/yolov9/releases/download/v0.1/gelan-c.pt
RUN wget -P yolov9/weights -q https://github.com/WongKinYiu/yolov9/releases/download/v0.1/gelan-e.pt
