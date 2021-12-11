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
import cv2
import numpy as np
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util
from multiprocessing import Process


def set_gpu():
    """限制显存大小
    如若不限制，则默认使用全部。
    对于低配计算机，容易造成卡死。比如 Jetson Nano 开发板的显存还是共用运存。
    """
    gpus= tf.config.list_physical_devices('GPU')
    if gpus:
        tf.config.experimental.set_virtual_device_configuration(
            gpus[0],
            [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=100)])
    print('已限制显存大小！')


@tf.function
def detect_fn(image):
    '''目标检测
    如果只是为了检测是否存在目标，只需要判断返回值中 detections['detection_scores'] 元素
    该元素为一个列表，为检测到的所有目标的相似度，可以设定一个阈值，存在大于该值即可认为存在指定目标 --- 即这里代表检测到锥桶
    '''
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections


if __name__ == '__main__':
    p_set_gpu = Process(target=set_gpu)
    p_set_gpu.start()

    # 加载模型
    configs = config_util.get_configs_from_pipeline_file('pipeline.config')
    detection_model = model_builder.build(model_config=configs['model'], is_training=False)
    ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
    ckpt.restore('ckpt-3').expect_partial()
    category_index = label_map_util.create_category_index_from_labelmap('label_map.pbtxt')
    print('已完成模型加载！')

    cam = cv2.VideoCapture(0)
    if cam.isOpened():
        print('打开摄像头成功！')
    else:
        print('打开摄像头失败！')
        exit(1)

    last = cv2.getTickCount()
    ret, img = cam.read()
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
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        label_id_offset = 1
        img_with_detections = img.copy()

        # 框出目标
        viz_utils.visualize_boxes_and_labels_on_image_array(
                    img_with_detections,
                    detections['detection_boxes'],  # 检测到物体的矩阵信息 [Ymin, Xmin, Ymax, Xmax], 数值范围在 0～1 之间
                    detections['detection_classes'] + label_id_offset,  # 检测到目标的 id (每个 id 对应一种目标物体 - 标签图)
                    detections['detection_scores'],  # 目标检测准确率
                    category_index,  # 标签和目标名对应关系
                    use_normalized_coordinates=True,
                    max_boxes_to_draw=5,  # 最多绘制的框数
                    min_score_thresh=0.80,  # 最小相似度
                    agnostic_mode=False)

        cv2.putText(img_with_detections, 'FPS:' + str(frame), (30, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))
        cv2.imshow('a', img_with_detections)
        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()
            break

    p_set_gpu.join()
    cam.release()