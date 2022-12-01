# Build envs

base docker images `nvcr.io/nvidia/pytorch:21.10-py3` 

### Build

```bash
docker pull nvcr.io/nvidia/pytorch:21.10-py3
```

**可选**
从docker文件夹下的Dockerfile构建镜像，基础镜像也是 `nvcr.io/nvidia/pytorch:21.10-py3`
*Run command in bash*

```bash
docker build . -t nvcr.io/nvidia/pytorch:21.10-py3-tf2
```

*or use `build.sh` *

```bash
cd /workspace/TensorRT-lab/envs/env1-pytorch-21.10
bash build.sh
```

### launch

use launch.sh

```bash
cd /workspace/TensorRT-lab/
bash launch.sh
```

**docker run**

```bash
docker run  --gpus all -p 8889:8889 --shm-size=8gb --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 -v /home/zhanglq/workspace/code/docker:/workspace/code --rm -it nvcr.io/nvidia/pytorch:21.10-py3 jupyter-lab --port=8889 --no-browser --ip 0.0.0.0 --allow-root  
```

or


```bash
docker run --name zhanglq --gpus all --shm-size=8gb --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 -v /home/zhanglq/workspace/:/workspace/  -it nvcr.io/nvidia/pytorch:21.10-py3-zhanglq
```

### 运行TensorRT8样例

+ 采用 TensorRT8 + Explicit batch 模式 + Dynamic Shape 模式 + BuilderConfig API + cuda-python 库的 Driver API / Runtime API 双版本
+ 运行方法

```shell
 cd ./TensorRT8
make test
```

+ 参考输出结果，见 ./trt-samples-for-hackathon-cn/cookbook/01-SimpleDemo/TensorRT8/result.log
