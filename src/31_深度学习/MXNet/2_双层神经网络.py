#!/usr/bin/env python3
"""
@file 2_双层神经网络.py

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
import pickle
import numpy as np
import matplotlib.pyplot as plt
import time
import logging
import mxnet as mx
import cv2


def cosCurve(x):
    """
    划分类别的边界
    """
    return 0.25 * np.sin(2 * x * np.pi + 0.5 * np.pi) + 0.5


def genData():
    """
    生成数据
    """
    np.random.seed(int(time.time()))
    
    samples = []  # 保存二维点的坐标
    labels = []  # 标明类别

    sampleDensity = 50  # 单位空间内平均样本数

    for i in range(sampleDensity):
        x1, x2 = np.random.random(2)
        bound = cosCurve(x1) # 计算 x1 对应的分类边界
        # 舍弃边界附近的样本，便于可视化
        if bound - 0.1 < x2 <= bound + 0.1:
            continue
        else:
            # 上半部分标签为 1，下半部分标签为 2
            samples.append((x1, x2))
            if x2 > bound:
                labels.append(1)
            else:
                labels.append(0)

    # 将生成的样本和标签保存
    with open('/tmp/data.pkl', 'wb') as f:
        pickle.dump((samples, labels), f)

    # 可视化
    for i, sample in enumerate(samples):
        plt.plot(sample[0], sample[1],
                 '+' if labels[i] else 'p',
                 mec='r' if labels[i] else 'b',
                 mfc='none',
                 markersize=10)

    x1 = np.linspace(0, 1)
    plt.plot(x1, cosCurve(x1), 'k--')
    plt.show()


def trainAndPredict():
    """
    训练和预测
    """
    data = mx.sym.Variable('data')  # 定义 data
    fc1 = mx.sym.FullyConnected(data=data, name='fc1', num_hidden=2)  # data 经过一个两输出的全连接层
    sigmoid1 = mx.sym.Activation(data=fc1, name='sigmoid1', act_type='sigmoid')  # 再经过一个 sigmoid 激活层
    fc2 = mx.sym.FullyConnected(data=sigmoid1, name='fc2', num_hidden=2)  # 再过一个全连接层
    mlp = mx.sym.SoftmaxOutput(data=fc2, name='softmax')  # 最后经过 Softmax 输出，自带 NLL 作为 loss 进行计算
    
    # multi layer perceptron  （mlp）多层感知机

    # 网络结构可视化
    shape = {'data': (2,)}
    mlpDot = mx.viz.plot_network(symbol=mlp, shape=shape)
    mlpDot.render('/tmp/simpleMlp.gv', view=False)  # 可见 /tmp/simpleMlp.gv.pdf， view 设置为 True 时会自动打开生成的 PDF 文件

    # 导入数据
    with open('/tmp/data.pkl', 'rb') as f:
        samples, labels = pickle.load(f)

    logging.getLogger().setLevel(logging.DEBUG)  # 设置 logging 级别，显示训练时信息

    batchSize = len(labels)
    samples = np.array(samples)
    labels = np.array(labels)

    trainIter = mx.io.NDArrayIter(samples, labels, batchSize)  # 生成训练数据迭代器

    # 训练网络
    model = mx.model.FeedForward.create(
        symbol=mlp,
        X=trainIter,
        num_epoch=1000,  # 迭代 1000 代
        learning_rate=0.1,  # 学习率
        momentum=0.99)  # 冲量系数

    '''
    # 另外一种方式训练模型
    model = mx.model.FeedForward(
        symbol=mlp,
        num_epoch=1000,
        learning_rate=0.1,
        momentum=0.99)
    model.fit(X=trainIter)
    '''

    # 用训练好的模型预测
    print(model.predict(mx.nd.array([[0.5, 0.5]])))

    # 取值范围平面的采样格点
    X = np.arange(0, 1.05, 0.05)
    Y = np.arange(0, 1.05, 0.05)
    X, Y = np.meshgrid(X, Y)

    grids = mx.nd.array([[X[i][j], Y[i][j]] for i in range(X.shape[0]) for j in range(X.shape[1])])  # 生成格点坐标
    gridProbs = model.predict(grids)[:, 1].reshape(X.shape)  # 获取模型预测的结果，以标签 1 为结果

    # 定义图标
    fig = plt.figure('样本页面')
    ax = fig.gca(projection='3d')

    # 画出整个结果的表面
    ax.plot_surface(X, Y, gridProbs, alpha=0.15, color='k', rstride=2, cstride=2, lw=0.5)
    samples0 = samples[labels==0]

    # 按照标签选出对应样本
    samples0_probs = model.predict(samples0)[:, 1]
    samples1 = samples[labels==1]
    samples1_probs = model.predict(samples1)[:, 1]

    # 按标签画出散点图
    ax.scatter(samples0[:, 0], samples0[:, 1], samples0_probs, c='b', marker='p', s=50)
    ax.scatter(samples1[:, 0], samples1[:, 1], samples1_probs, c='r', marker='+', s=50)

    plt.show()


if __name__ == '__main__':
    genData()
    cv2.waitKey(0)
    trainAndPredict()
