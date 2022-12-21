# 官方镜像库拉取基础镜像
FROM pytorch/pytorch:1.12.1-cuda11.3-cudnn8-devel 

SHELL ["/bin/bash", "-c"]
# Setup user account
ARG uid=1000
ARG gid=1000
ARG USER_NAME="devel"
RUN groupadd -r -f -g ${gid} ${USER_NAME} && useradd -o -r -l -u ${uid} -g ${gid} -ms /bin/bash ${USER_NAME}
RUN usermod -aG sudo ${USER_NAME}
RUN echo ${USER_NAME}:${USER_NAME}@developer | chpasswd
RUN chown ${USER_NAME} /workspace

# Repair the GPG signing key rotation for CUDA repositories
# https://github.com/NVIDIA/cuda-repo-management/issues/4
# RUN rm /etc/apt/sources.list.d/cuda.list
# RUN rm /etc/apt/sources.list.d/nvidia-ml.list
# RUN apt-key del 7fa2af80
RUN apt-get update && apt-get install -y --no-install-recommends wget
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.0-1_all.deb
RUN dpkg -i cuda-keyring_1.0-1_all.deb

# Install requried libraries
RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:ubuntu-toolchain-r/test

RUN apt-get update && apt-get install -y --no-install-recommends \
    git-lfs \
    # libeigen3-dev \
    sudo

RUN cd /usr/local/bin &&\
    ln -s /usr/bin/python3 python &&\
    ln -s /opt/conda/bin/pip pip;

# Install PyPI packages
RUN pip3 config set global.index-url https://pypi.mirrors.ustc.edu.cn/simple/
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
# Workaround to remove numpy installed with tensorflow
RUN pip3 install --upgrade numpy
RUN pip3 install "opencv-python-headless<4.3"

# 设置语言环境为中文，防止 print 中文报错
ENV LANG C.UTF-8
USER ${USER_NAME}
WORKDIR /workspace
RUN ["/bin/bash"]