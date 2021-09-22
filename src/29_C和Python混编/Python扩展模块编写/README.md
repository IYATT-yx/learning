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
