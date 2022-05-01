import os

import keras.models
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
from math import sin, cos, pi
from AngleAnnotation import AngleAnnotation
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
    # resized_and_converted_image = convertImage(image)
    # plt.imshow(resized_and_converted_image, cmap='gray')
    fig,axis=plt.subplots()
    plt.imshow(image)
    width, height = get_width_height_of_np_array(image)

    print(prediction)
    print(prediction[0::2])
    print(prediction[1::2])

    x_values = prediction[0::2]
    y_values = prediction[1::2]

    x_values_scaled = []
    y_values_scaled = []
    print(x_values.shape)
    for idx in range(x_values.shape[0]):
        x_scaled, y_scaled = scale_points(width, height, x_values[idx], y_values[idx])
        x_values_scaled.append(x_scaled)
        y_values_scaled.append(y_scaled)

    print(x_values)
    print(y_values)
    print(x_values_scaled)
    print(y_values_scaled)

    first_line = [[x_values_scaled[0], x_values_scaled[1]], [y_values_scaled[0], y_values_scaled[1]]]
    second_line = [[x_values_scaled[1], x_values_scaled[2]], [y_values_scaled[1], y_values_scaled[2]]]
    third_line = [[x_values_scaled[2], x_values_scaled[3]], [y_values_scaled[2], y_values_scaled[3]]]

    intersection_point_1=(x_values_scaled[1],y_values_scaled[1])
    angle1=get_angle(np.array([x_values_scaled[0],y_values_scaled[0]]), np.array([x_values_scaled[1], y_values_scaled[1]]),np.array([x_values_scaled[2],y_values_scaled[2]]))
    am1 = AngleAnnotation(intersection_point_1, (x_values_scaled[2], y_values_scaled[2]),(x_values_scaled[0],y_values_scaled[0]), ax=axis, size=20, text=str(angle1), textposition="inside",
                          text_kw=dict(fontsize=3, xytext=(10, -5),color="blue"))

    intersection_point_2=(x_values_scaled[2],y_values_scaled[2])
    angle2=get_angle(np.array([x_values_scaled[1], y_values_scaled[1]]),np.array([x_values_scaled[2],y_values_scaled[2]]),np.array([x_values_scaled[3],y_values_scaled[3]]) )
    am2 = AngleAnnotation(intersection_point_2,(x_values_scaled[3], y_values_scaled[3]), (x_values_scaled[1], y_values_scaled[1]), ax=axis, size=20, text=str(angle2), textposition="inside",
                          text_kw=dict(fontsize=3, xytext=(10, -5),color="blue"))

    plt.plot(first_line[0], first_line[1], 'r-', linewidth=0.6, marker='x')
    plt.plot(second_line[0], second_line[1], 'r-', linewidth=0.6, marker='x')
    plt.plot(third_line[0], third_line[1], 'r-', linewidth=0.6, marker='x')

    left_acetabulum = np.array(x_values[0], y_values[0])
    left_femoral = np.array(x_values[1], y_values[1])
    right_femoral = np.array(x_values[2], y_values[2])
    right_acetabulum = np.array(x_values[3], y_values[3])

    # plt.plot(first_line[0][0], first_line[1][0], first_line[0][1], first_line[1][1], 'b-', marker='x')
    # plt.plot(second_line[0][0], second_line[1][0], second_line[0][1], second_line[1][1], 'b-', marker='x')
    # plt.plot(third_line[0][0], third_line[1][0], third_line[0][1], third_line[1][1], 'b-', marker='x')

    # plt.scatter(prediction[0::2], prediction[1::2], marker='x', s=20)
    plt.axis("off")

    plt.savefig('./static/predictions/' + new_image_name + ".jpg")
    plt.close()
    plt.show()
    return angle1, angle2

def scale_points(image_width, image_height, point_x, point_y, processed_image_width=512, processed_image_height=512):
    """
    :param image_width: Width of initial resized_and_converted_image
    :param image_height: Height of initial image
    :param processed_image_width: Width of processed image, 512 currently
    :param processed_image_height: Height of processed image, 512 currently
    :param point_x: X coordinate of point
    :param point_y: Y coordinate of point
    :return: The corresponding (x,y) of the point if it were to be situated in the same place, but on the other image
    """
    return point_x * image_width / processed_image_width, point_y * image_height / processed_image_height


def get_width_height_of_np_array(image):
    dimensions = image.shape
    return dimensions[1], dimensions[0]

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

def get_angle(p0, p1=np.array([0,0]), p2=None):
    ''' compute angle (in degrees) for p0p1p2 corner
    Inputs:
        p0,p1,p2 - points in the form of [x,y]
    '''
    if p2 is None:
        p2 = p1 + np.array([1, 0])
    v0 = np.array(p0) - np.array(p1)
    v1 = np.array(p2) - np.array(p1)

    angle = np.math.atan2(np.linalg.det([v0,v1]),np.dot(v0,v1))
    return np.degrees(angle)
