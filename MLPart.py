import os

import keras.models
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
from math import sin, cos, pi

import tensorflow
from keras.applications.resnet import ResNet50
from keras.layers import Conv2D, LeakyReLU, GlobalAveragePooling2D, Dropout, Dense
from keras.models import Sequential


def load_own_model(directory):
    return keras.models.load_model(directory)


def convertImage(img):
    # image might need to be normalized
    color = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    resize = cv2.resize(color, dsize=(512, 512), interpolation=cv2.INTER_CUBIC)
    return np.reshape(resize, (512, 512, 1))


def resize_image(img):
    resize = cv2.resize(img, dsize=(512, 512), interpolation=cv2.INTER_CUBIC)
    return np.reshape(resize, (512, 512, 1))


def predict_image(image, model, new_image_name):
    image_for_model = [convertImage(image)]
    image_for_model = np.array(image_for_model) / 255.
    prediction = model.predict(image_for_model)[0]
    image = convertImage(image)
    plt.imshow(image, cmap='gray')
    print(prediction)
    print(prediction[0::2])
    print(prediction[1::2])

    x_values = prediction[0::2]
    y_values = prediction[1::2]

    first_line = [[x_values[0], x_values[1]], [y_values[0], y_values[1]]]
    second_line = [[x_values[1], x_values[2]], [y_values[1], y_values[2]]]
    third_line = [[x_values[2], x_values[3]], [y_values[2], y_values[3]]]

    plt.plot(first_line[0], first_line[1], 'r-', linewidth=0.6, marker='x')
    plt.plot(second_line[0], second_line[1], 'r-', linewidth=0.6, marker='x')
    plt.plot(third_line[0], third_line[1], 'r-', linewidth=0.6, marker='x')

    left_acetabulum=np.array(x_values[0],y_values[0])
    left_femoral=np.array(x_values[1],y_values[1])
    right_femoral=np.array(x_values[2],y_values[2])
    right_acetabulum=np.array(x_values[3],y_values[3])

    print(angle_between(left_acetabulum, left_femoral, right_femoral))
    print(angle_between(left_femoral,right_femoral,right_acetabulum))


    # plt.plot(first_line[0][0], first_line[1][0], first_line[0][1], first_line[1][1], 'b-', marker='x')
    # plt.plot(second_line[0][0], second_line[1][0], second_line[0][1], second_line[1][1], 'b-', marker='x')
    # plt.plot(third_line[0][0], third_line[1][0], third_line[0][1], third_line[1][1], 'b-', marker='x')

    # plt.scatter(prediction[0::2], prediction[1::2], marker='x', s=20)
    plt.savefig('./static/predictions/' + new_image_name + ".jpg")
    plt.close()
    plt.show()

def angle_between(a,b,c):
    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)

    return np.degrees(angle)

#
# def plot_sample(image, keypoint, axis, title):
#     image = image.reshape(512, 512)
#     axis.imshow(image)
#     axis.scatter(keypoint[0::2], keypoint[1::2], marker='x', s=20)
#     plt.title(title)
#
#
# model2 = keras.models.load_model("currentModel")
# predict = model2.predict()
# plot_sample(test_images[i], predict[i], axis, "Test prediction")
