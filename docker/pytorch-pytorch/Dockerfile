ARG CUDA_VERSION=11.4.2
ARG CUDNN_VERSION=8
ARG OS_VERSION=20.04

# 从nvidia 官方镜像库拉取基础镜像
FROM pytorch/pytorch:cuda11.3-cudnn8-devel 
LABEL maintainer=""

ENV TRT_VERSION 8.2.5.1
SHELL ["/bin/bash", "-c"]

# Setup user account
ARG uid=1000
ARG gid=1000
ARG USER_NAME="trtusr"
RUN groupadd -r -f -g ${gid} ${USER_NAME} && useradd -o -r -l -u ${uid} -g ${gid} -ms /bin/bash ${USER_NAME}
RUN usermod -aG sudo ${USER_NAME}
RUN echo ${USER_NAME}:${USER_NAME}@nvidia | chpasswd
RUN chown ${USER_NAME} /workspace

# Repair the GPG signing key rotation for CUDA repositories
# https://github.com/NVIDIA/cuda-repo-management/issues/4
# RUN rm /etc/apt/sources.list.d/cuda.list
# RUN rm /etc/apt/sources.list.d/nvidia-ml.list
# RUN apt-key del 7fa2af80
# RUN apt-get update && apt-get install -y --no-install-recommends wget
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.0-1_all.deb
RUN dpkg -i cuda-keyring_1.0-1_all.deb

# 将 apt 的升级源切换成 阿里云
# RUN  sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list && \
#     apt-get clean && \
#     rm /etc/apt/sources.list.d/*

RUN apt-get update && apt-get install -y --no-install-recommends \
    git-lfs \
    # libeigen3-dev \
    sudo

# # 安装 TensorRT
# RUN cd /tmp && sudo apt-get update

# # Install TensorRT
# RUN if [ "${CUDA_VERSION}" = "10.2" ] ; then \
#     v="${TRT_VERSION%.*}-1+cuda${CUDA_VERSION}" &&\
#     apt-get update &&\
#     sudo apt-get install libnvinfer8=${v} libnvonnxparsers8=${v} libnvparsers8=${v} libnvinfer-plugin8=${v} \
#     libnvinfer-dev=${v} libnvonnxparsers-dev=${v} libnvparsers-dev=${v} libnvinfer-plugin-dev=${v} \
#     python3-libnvinfer=${v}; \
#     else \
#     v="${TRT_VERSION%.*}-1+cuda${CUDA_VERSION%.*}" &&\
#     apt-get update &&\
#     apt-get install libnvinfer8=${v} libnvonnxparsers8=${v} libnvparsers8=${v} libnvinfer-plugin8=${v} \
#     libnvinfer-dev=${v} libnvonnxparsers-dev=${v} libnvparsers-dev=${v} libnvinfer-plugin-dev=${v} \
#     python3-libnvinfer=${v}; \
#     fi

# # 阻止tensorrt自动升级
# RUN apt-mark hold libnvinfer8 libnvonnxparsers8 libnvparsers8 libnvinfer-plugin8 libnvinfer-dev libnvonnxparsers-dev libnvparsers-dev libnvinfer-plugin-dev python3-libnvinfer

# # 如果想要升级最新版本的tensorrt 
# sudo apt-mark unhold libnvinfer8 libnvonnxparsers8 libnvparsers8 libnvinfer-plugin8 libnvinfer-dev libnvonnxparsers-dev libnvparsers-dev libnvinfer-plugin-dev python3-libnvinfer


# Install PyPI packages
RUN pip3 config set global.index-url https://pypi.douban.com/simple/
RUN pip3 install "opencv-python-headless<4.3"


# 设置语言环境为中文，防止 print 中文报错
ENV LANG C.UTF-8

USER ${USER_NAME}
RUN ["/bin/bash"]