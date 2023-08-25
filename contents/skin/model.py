"""
Purpose: Generate the skin(N x N) from a single image(aligned image)
Process: De-lighting > 468-landmarks > extracting ROI > !TBD!
Input: 1024^2 a facial image
Output: N^2 matrix
"""
import os
import cv2
import copy
import math
import numpy as np
from typing import Tuple
from contents.external.landmarker import FaceLandMarks


def delighting(source: np.ndarray) -> np.ndarray:
    """
    :param source: cv2 image (bgr, w,h, c)
    :return: cv2 image
    :refer to https://t9t9.com/60
    """
    lab = cv2.cvtColor(source, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    # blur l-channel image, then invert blurred image
    blur = 255 - cv2.medianBlur(l, ksize=25)
    # blending
    delight = cv2.addWeighted(l, 0.7, blur, 0.3, 0)
    target = cv2.merge((delight, a, b))
    return cv2.cvtColor(target, cv2.COLOR_LAB2RGB)


class Patcher:
    def __init__(self, output_size, debug, **kwargs):
        self.detector = FaceLandMarks()
        self.output_size = tuple(output_size)
        self.debug = debug
        self.lt = 116
        self.rb = 205

    def __call__(self, sample):
        index, image_path = sample
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        image = delighting(image)
        try:
            landmarks = self.get_landmarks(copy.deepcopy(image))
            raw, roi = self.cut_roi(image, landmarks)

            if self.debug:
                # test = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                # cv2.imwrite(sample[1].replace('aligned', 'debug_delight'), test)
                test = cv2.cvtColor(roi, cv2.COLOR_RGB2BGR)
                cv2.imwrite(sample[1].replace('aligned', 'debug_roi'), test)

            result = {
                'index': index,
                'input_image': image,
                'input_shape': image.shape,
                'input_path': image_path,
                'skin': roi,
                'skin_shape': roi.shape
            }
            return result
        except Exception as e:
            print('Exception message: ', e)
            print('[Info] path: ' + image_path)
            os.remove(image_path)
            os.remove(image_path.replace('aligned', 'image'))
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(image_path.replace('aligned', 'bin'), image)
            return None

    def get_landmarks(self, image: np.ndarray) -> np.ndarray:
        img, faces, landmarks = self.detector.findFaceLandmark(image)
        return landmarks[0]

    def cut_roi(self, image: np.ndarray, landmarks: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        h, w, c = image.shape
        left_top = landmarks[self.lt]
        right_bottom = landmarks[self.rb]

        x_px = min(math.floor(left_top[0] * w), w - 1)
        y_px = min(math.floor(left_top[1] * h), h - 1)
        width = math.floor(abs(right_bottom[0] - left_top[0]) * w)
        height = math.floor(abs(left_top[1] - right_bottom[1]) * h)

        source_roi = image[y_px:y_px + height, x_px:x_px + width]
        resized_roi = cv2.resize(source_roi, dsize=self.output_size, interpolation=cv2.INTER_AREA)
        return source_roi, resized_roi
