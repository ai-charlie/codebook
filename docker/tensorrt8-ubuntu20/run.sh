Project_Path=~/workspace/face_api
IMAGE_NAME=tensorrt:trt8.5.1-cu11.3-ubuntu2004
CONTAINER_NAME=tensorrt-py38
docker run --gpus all \
--name $CONTAINER_NAME \
--shm-size=8gb --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 \
-v $Project_Path:/workspace/ -it $IMAGE_NAME \
-p 7009:7009 \
# jupyter-lab --port=8888 --no-browser --ip 0.0.0.0 --allow-root  