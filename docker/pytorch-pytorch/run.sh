Project_Path=$PWD
IMAGE_NAME=pytorch:pytorch-cuda11.3-cudnn8-devel
CONTAINER_NAME=pytorch-devel

docker run  --gpus all \
--name $CONTAINER_NAME \
--shm-size=8gb --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 \
-v $Project_Path:/workspace -it $IMAGE_NAME \
# jupyter-lab --port=8889 --no-browser --ip 0.0.0.0 --allow-root