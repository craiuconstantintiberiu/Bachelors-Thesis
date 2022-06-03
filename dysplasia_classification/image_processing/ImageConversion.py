import cv2
import numpy as np


def convertImage(img, newX=224, newY=224):
    # image might need to be normalized
    color = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    resize = cv2.resize(color, dsize=(newX, newY), interpolation=cv2.INTER_CUBIC)
    reshape = np.reshape(resize, (newX, newY, 1))
    normalized = reshape / 255.0
    return np.array([normalized])

