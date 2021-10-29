'''
 * file: cone-bucket-detection.py
 * describe: 锥桶检测
 * site: github.com/IYATT-yx/learning
 *
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
'''
# pip3 install opencv-python==4.5.3.56
import cv2
import numpy as np
#########################################################################
# 有 GPU 硬件
# NVIDIA 驱动：https://www.nvidia.cn/geforce/drivers/
# CUDA：https://developer.nvidia.com/cuda-downloads
# cuDNN：https://developer.nvidia.com/rdp/cudnn-archive#a-collapse51b
# 安装 GPU 版 TensorFlow： pip3 install tensorflow==2.6.0
#########################################################################
# 无 GPU 支持： pip3 install tensorflow-gpu==2.6.0
import tensorflow as tf
################################################################################################################################################
# Tensorlow Object Detection
# sudo apt install protobuf-compiler
# git clone https://github.com/tensorflow/models
# cd models/research && protoc object_detection/protos/*.proto --python_out=. && cp object_detection/packages/tf2/setup.py . && pip3 install . 
################################################################################################################################################
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util


gpus= tf.config.list_physical_devices('GPU')
if gpus:
    tf.config.experimental.set_virtual_device_configuration(
        gpus[0],
        [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=512)])  # 限制显存 - 否则默认会尝试使用全部


@tf.function
def detect_fn(image):
    '''目标检测
    '''
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections


if __name__ == '__main__':
    # 加载模型
    configs = config_util.get_configs_from_pipeline_file('pipeline.config')
    detection_model = model_builder.build(model_config=configs['model'], is_training=False)
    ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
    ckpt.restore('ckpt-3').expect_partial()
    category_index = label_map_util.create_category_index_from_labelmap('label_map.pbtxt')

    cam = cv2.VideoCapture('cone-bucket.avi')  # 测试视频
    # cam = cv2.VideoCapture(0)  # 使用摄像头

    last = cv2.getTickCount()
    while True:
        # 帧率计算
        now = cv2.getTickCount()
        frame = int(cv2.getTickFrequency() / (now - last))
        last = now
        # 图像获取
        ret, img = cam.read()
        if img is None:
            break

        input_tensor = tf.convert_to_tensor(np.expand_dims(img, 0), dtype=tf.float32)
        detections = detect_fn(input_tensor)

        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
        detections['num_detections'] = num_detections
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        label_id_offset = 1
        img_with_detections = img.copy()

        viz_utils.visualize_boxes_and_labels_on_image_array(
                    img_with_detections,
                    detections['detection_boxes'],  # 检测到物体的矩阵信息 [Ymin, Xmin, Ymax, Xmax], 数值范围在 0～1 之间
                    detections['detection_classes'] + label_id_offset,  # 检测到目标的 id (每个 id 对应一种目标物体 - 标签图)
                    detections['detection_scores'],  # 目标检测准确率
                    category_index,  # 标签图
                    use_normalized_coordinates=True,
                    max_boxes_to_draw=5,  # 最多绘制的框数
                    min_score_thresh=0.9,  # 绘制的最小得分
                    agnostic_mode=False)

        cv2.putText(img_with_detections, 'FPS:' + str(frame), (30, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))
        cv2.imshow('a', img_with_detections)
        if cv2.waitKey(1) == 27:
            break
    cam.release()