# MXNet 安装

```bash
sudo apt install -y ccache cmake build-essential git libatlas-base-dev graphviz

git clone --recursive  https://github.com/apache/incubator-mxnet.git --branch=1.8.0

cd incubator-mxnet && mkdir build && cd build

cmake -DUSE_CUDA=ON -DUSE_CUDNN=ON -DUSE_CPP_PACKAGE=ON -DBUILD_CPP_EXAMPLES=OFF -DUSE_BLAS=atlas -DCMAKE_CUDA_COMPILER=/usr/local/cuda/bin/nvcc -DCMAKE_BUILD_TYPE=release -G'Unix Makefiles' ..

make -j8

sudo make install

cd python

sudo python3 setup.py install
```
