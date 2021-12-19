#!/usr/bin/env python3
"""
@file mnist-数据集预处理.py

 * Copyright (C) 2021 IYATT-yx (Zhao Hongfei, 赵洪飞)，2514374431@qq.com
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import os
import sys
import pickle
import gzip
import matplotlib.pyplot as plt
import argparse


absPath = os.path.dirname(os.path.abspath(__file__))
imgsDir = '/tmp/mnist'  # 数据路径


def convert():
    """
    转换数据集
    提取图片和标签
    """
    print('正在从 mnist.pkl.gz 导入数据......')
    with gzip.open(absPath + '/mnist.pkl.gz', 'rb') as f:
        trainSet, validSet, testSet = pickle.load(f, encoding='bytes')
    os.system('rm -rf {}'.format(imgsDir))
    os.makedirs(imgsDir)
    datasets = {'train': trainSet, 'val': validSet, 'test': testSet}
    for dataname, dataset in datasets.items():
        dataDir = os.sep.join([imgsDir, dataname])
        os.makedirs(dataDir)
        print('开始转换 {} 数据集({})：'.format(dataname, dataDir))
        for i, (img, label) in enumerate(zip(*dataset)):
            filename = '{:0>6d}_{}.jpg'.format(i, label)
            filepath = os.sep.join([dataDir, filename])
            img = img.reshape((28, 28))
            plt.imsave(filepath, img, cmap='gray')
            if (i+1) % 10000 == 0:
                print('{} 张图片已转换!'.format(i+1))

listFiles = []
lists = []
def genImgList_mxnet():
    """
    生成标签 - MXNet
    整数编号\t标签\t文件路径
    """
    for dir in os.listdir(imgsDir):
        absDir = os.sep.join([imgsDir, dir])
        if not os.path.isdir(absDir):
            continue
        filenames = os.listdir(absDir)
        listFile = absDir + '_mxnet.lst'
        listFiles.append(listFile)
        lists.append(dir)
        with open(listFile, 'w') as f:
            for i, filename in enumerate(filenames):
                filepath = os.sep.join([absDir, filename])
                label = filename[:filename.rfind('.')].split('_')[1]
                line = '{}\t{}\t{}\n'.format(i, label, filepath)
                f.write(line)
        print('已生成: {}'.format(listFile))

def parseArgs():
    """定义所有参数
    返回容纳所有参数的对象
    """
    paser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='mnist 数据集预处理')
    paser.add_argument('frame', help='深度学习框架类型：mnist、caffe')
    return paser.parse_args()



if __name__ == '__main__':
    args = parseArgs()
    if args.frame == 'mxnet':
        convert()
        genImgList_mxnet()
        for listFile, list in zip(listFiles, lists):
            cmd = '{} --num-thread 8 {} {}'.format(absPath + '/im2rec.py', listFile, os.path.dirname(listFile))
            print(cmd)  # im2rec.py 文件取自于 MXNet 源码（https://github.com/apache/incubator-mxnet） tools 目录下
            os.system(cmd)
    elif args.frame == 'caffe':  # 暂未实现
        pass
    else:
        print('无法识别的参数！')
