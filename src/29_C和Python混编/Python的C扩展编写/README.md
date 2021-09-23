注：  
Linux 下默认 python 和 pip 命令对应版本为 2.x 即 python2 和 pip2，要使用 3.x 版本需要使用命令 python3 和 pip3。然而在 Windows 下，安装 Python3 后，直接使用 python 和 pip 就对应是 3.x 了。所以下面的参考命令操作在 Windows 下执行的话，请换为 python 和 pip。  

1.构建测试  
```bash
# 会在当前路径下生成 py 可直接导入的库文件
python3 setup.py build_ext --inplace
```

2.安装使用  
* 源码直接安装
```bash
# 安装
python3 setup.py build && sudo python3 setup.py install --record installPaths.txt

# 卸载
cat installPaths.txt | sudo xargs rm -rf && rm installPaths.txt
```

* 打包安装
```bash
# 发布源码包
python3 setup.py sdist

# 安装
pip3 install dist/MD5-1.0.tar.gz

# 卸载
pip3 uninstall -y md5
```

```bash
# 安装依赖
pip3 install wheel

# 发布二进制包
pip3 wheel --wheel-dir=build .

# 安装
pip3 install build/[xxxxxxxx].whl

# 卸载
pip3 uninstall -y md5
```

```bash
# 构建 Windows 二进制安装包
python setup.py bdist_wininst
```