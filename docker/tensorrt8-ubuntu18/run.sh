Project_Path=/data/workspace/zhanglq/
IMAGE_NAME=tensorrt:trt8.5.1-cu10.2-ubuntu1804-py38
CONTAINER_NAME=tensorrt

docker run  --gpus all \
--name $CONTAINER_NAME \
--shm-size=8gb --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 \
-v $Project_Path:/workspace/code -it $IMAGE_NAME \
# jupyter-lab --port=8889 --no-browser --ip 0.0.0.0 --allow-root