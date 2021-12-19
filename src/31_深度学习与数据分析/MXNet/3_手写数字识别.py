#!/usr/bin/env python3
"""
@file 3_手写数字识别.py

    基于 CNN （LeNet-5)

    需要先生成数据 - 使用 data/mnist/mnist-数据集预处理.py 生成

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
import mxnet as mx
import logging
import os
import time
import cv2
import numpy as np
from collections import namedtuple
Batch = namedtuple('Batch', ['data'])

absPath = os.path.dirname(os.path.abspath(__file__))

def train():
    """训练 LeNet-5
    """
    data = mx.symbol.Variable('data')  # 定义数据

    # 第一层卷积和池化
    conv1 = mx.symbol.Convolution(data=data, kernel=(5, 5), num_filter=20)
    pool1 = mx.symbol.Pooling(data=conv1, pool_type="max",
                            kernel=(2, 2), stride=(2, 2))
    # 第二层卷积和池化
    conv2 = mx.symbol.Convolution(data=pool1, kernel=(5, 5), num_filter=50)
    pool2 = mx.symbol.Pooling(data=conv2, pool_type="max",
                            kernel=(2, 2), stride=(2, 2))
    # 第一层全连接
    flatten = mx.symbol.Flatten(data=pool2)  # 展开二维数据
    fc1 = mx.symbol.FullyConnected(data=flatten, num_hidden=500)
    relu1 = mx.symbol.Activation(data=fc1, act_type="relu")

    # 第二层全连接
    fc2 = mx.symbol.FullyConnected(data=relu1, num_hidden=10)

    # loss
    lenet5 = mx.symbol.SoftmaxOutput(data=fc2, name='softmax')

    trainDataiter = mx.io.ImageRecordIter(
        path_imgrec="/tmp/mnist/train_mxnet.rec",
        data_shape=(1, 28, 28),  # 数据维度
        batch_size=50,  # 批的样本数量
        mean_r=128,  # 减去均值，因为是单通道，所以定义通道均值即可
        scale=0.00390625,  # 减去均值后归一化到 [0.5, 0.5) 之间
        rand_crop=True,  # 数据增加，随即剪裁
        min_crop_size=26,  # 剪裁的最小边长
        max_crop_size=28,  # 剪裁的最大边长
        max_rotate_angle=15,  # 数据增加，随机旋转 -15度～15度
        fill_value=0  # 旋转后的空白部分填充为 0（黑色）
    )

    valDataiter = mx.io.ImageRecordIter(
        path_imgrec="/tmp/mnist/val_mxnet.rec",
        data_shape=(1, 28, 28),
        batch_size=100,
        mean_r=128,
        scale=0.00390625,
    )

    # 把日志输出到文件
    logging.getLogger().setLevel(logging.DEBUG)
    fh = logging.FileHandler('/tmp/mnist/train-mnist-lenet.log')
    logging.getLogger().addHandler(fh)

    # 根据训练进程改变学习率
    lrScheduler = mx.lr_scheduler.FactorScheduler(1000, factor=0.95)
    optimizer_params = {
        'learning_rate': 0.01,
        'momentum': 0.9,
        'wd': 0.0005,
        'lr_scheduler': lrScheduler
    }

    checkpoint = mx.callback.do_checkpoint('/tmp/mnist/mnist-lenet-model', period=5)  # 回调函数 - 每 5 个 epoch 保存一个模型
    mod = mx.mod.Module(lenet5, context=mx.gpu(0))
    mod.fit(trainDataiter,
            eval_data=valDataiter,
            optimizer_params=optimizer_params,
            num_epoch=36,
            epoch_end_callback=checkpoint)


def score():
    """测试模型准确率
    """
    testDataiter = mx.io.ImageRecordIter(
        path_imgrec="/tmp/mnist/test_mxnet.rec",
        data_shape=(1, 28, 28),
        batch_size=100,
        mean_r=128,
        scale=0.00390625,
    )

    mod = mx.mod.Module.load('/tmp/mnist/mnist-lenet-model', 35, context=mx.gpu(0))  # 读取第 35 代模型
    mod.bind(
        data_shapes=testDataiter.provide_data, 
        label_shapes=testDataiter.provide_label, 
        for_training=False)

    '''
    # 如果我们需要从第35代开始训练
    mod.fit(...,
            arg_params=arg_params,
            aux_params=aux_params,
            begin_epoch=35)
    '''

    metric = mx.metric.create('acc')  # 评估准确率 accuracy
    mod.score(testDataiter, metric)

    for name, val in metric.get_name_value():
        print('{}={:.2f}%'.format(name, val*100))


def benchmark():
    """预测结果
    """
    benchmarkDataiter = mx.io.ImageRecordIter(
        path_imgrec="/tmp/mnist/test_mxnet.rec",
        data_shape=(1, 28, 28),
        batch_size=64,
        mean_r=128,
        scale=0.00390625,
    )

    mod = mx.mod.Module.load('/tmp/mnist/mnist-lenet-model', 35, context=mx.gpu(0))
    mod.bind(
        data_shapes=benchmarkDataiter.provide_data, 
        label_shapes=benchmarkDataiter.provide_label, 
        for_training=False)

    start = time.time()
    for i, batch in enumerate(benchmarkDataiter):
        mod.forward(batch)
    time_elapsed = time.time() - start
    msg = '{} 次迭代!\n平均每次前向计算消耗时间: {:.6f} ms'
    print(msg.format(i+1, 1000*time_elapsed/float(i)))


def recognize():
    """识别数字
    """
    inputPath = '/tmp/mnist/test'

    mod = mx.mod.Module.load('/tmp/mnist/mnist-lenet-model', 35, context=mx.gpu(0))
    mod.bind(
        data_shapes=[('data', (1, 1, 28, 28))], 
        for_training=False)

    filenames = os.listdir(inputPath)
    for filename in filenames:
        filepath = os.sep.join([inputPath, filename])
        img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
        img = (img.astype(np.float)-128) * 0.00390625
        img = img.reshape((1, 1)+img.shape)
        mod.forward(Batch([mx.nd.array(img)]))
        prob = mod.get_outputs()[0].asnumpy()
        prob = np.squeeze(prob)
        pred_label = np.argmax(prob)
        print('Predicted digit for {} is {}'.format(filepath, pred_label))


if __name__ == '__main__':
    train()
    cmd = 'python3 {} --log-file=/tmp/mnist/train-mnist-lenet.log'.format(absPath + '/training_curves.py')  #  绘制训练过程中的准确率图
    print(cmd)
    os.system(cmd)
    score()
    benchmark()
    recognize()