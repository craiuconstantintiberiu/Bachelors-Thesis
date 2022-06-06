import numpy as np
from matplotlib import pyplot as plt

from ..image_processing.AngleAnnotation import AngleAnnotation


class ImageAnnotator:
    @staticmethod
    def retrieve_angles(prediction):
        x_values, y_values = ImageAnnotator.obtain_x_and_y_values(prediction)
        left_hip_angle, right_hip_angle = ImageAnnotator.obtain_hip_angles(x_values, y_values)
        return left_hip_angle, right_hip_angle

    @staticmethod
    def obtain_x_and_y_values(prediction):
        x_values = prediction[0::2]
        y_values = prediction[1::2]
        return x_values, y_values

    @staticmethod
    def save_annotated_radiograph(image, new_image_name, left_hip_angle, right_hip_angle, prediction):
        width, height = image.shape[1], image.shape[0]
        x_values, y_values = ImageAnnotator.obtain_x_and_y_values(prediction)
        x_values_scaled, y_values_scaled = ImageAnnotator.scale_x_and_y_values(height, width, x_values, y_values)
        fig, axis = plt.subplots()
        plt.imshow(image)
        ImageAnnotator.plot_lines_between_keypoints(x_values_scaled, y_values_scaled)
        ImageAnnotator.plot_hip_angle_arcs(axis, left_hip_angle, right_hip_angle, x_values_scaled, y_values_scaled)
        plt.axis("off")
        plt.savefig('./static/predictions/' + new_image_name + ".svg", bbox_inches='tight', pad_inches=0)
        plt.close()
        plt.show()

    @staticmethod
    def plot_hip_angle_arcs(axis, left_hip_angle, right_hip_angle, x_values_scaled, y_values_scaled):
        intersection_point_1 = (x_values_scaled[1], y_values_scaled[1])
        AngleAnnotation(intersection_point_1, (x_values_scaled[2], y_values_scaled[2]),
                        (x_values_scaled[0], y_values_scaled[0]), ax=axis, size=20, text=str(left_hip_angle),
                        textposition="inside",
                        text_kw=dict(fontsize=3, color="blue"))
        intersection_point_2 = (x_values_scaled[2], y_values_scaled[2])
        AngleAnnotation(intersection_point_2, (x_values_scaled[3], y_values_scaled[3]),
                        (x_values_scaled[1], y_values_scaled[1]), ax=axis, size=20, text=str(right_hip_angle),
                        textposition="inside",
                        text_kw=dict(fontsize=3, color="blue"))

    @staticmethod
    def obtain_hip_angles(x_values_scaled, y_values_scaled):
        angle1 = ImageAnnotator.get_angle(np.array([x_values_scaled[0], y_values_scaled[0]]),
                                          np.array([x_values_scaled[1], y_values_scaled[1]]),
                                          np.array([x_values_scaled[2], y_values_scaled[2]]))
        angle2 = ImageAnnotator.get_angle(np.array([x_values_scaled[1], y_values_scaled[1]]),
                                          np.array([x_values_scaled[2], y_values_scaled[2]]),
                                          np.array([x_values_scaled[3], y_values_scaled[3]]))
        return round(angle1, 2), round(angle2, 2)

    @staticmethod
    def plot_lines_between_keypoints(x_values_scaled, y_values_scaled):
        first_line = [[x_values_scaled[0], x_values_scaled[1]], [y_values_scaled[0], y_values_scaled[1]]]
        second_line = [[x_values_scaled[1], x_values_scaled[2]], [y_values_scaled[1], y_values_scaled[2]]]
        third_line = [[x_values_scaled[2], x_values_scaled[3]], [y_values_scaled[2], y_values_scaled[3]]]
        plt.plot(first_line[0], first_line[1], 'r-', linewidth=0.6)
        plt.plot(second_line[0], second_line[1], 'r-', linewidth=0.6)
        plt.plot(third_line[0], third_line[1], 'r-', linewidth=0.6)

    @staticmethod
    def scale_x_and_y_values(height, width, x_values, y_values):
        x_values_scaled = []
        y_values_scaled = []
        for idx in range(len(x_values)):
            x_scaled, y_scaled = ImageAnnotator.scale_points(width, height, x_values[idx], y_values[idx])
            x_values_scaled.append(x_scaled)
            y_values_scaled.append(y_scaled)
        return x_values_scaled, y_values_scaled

    @staticmethod
    def scale_points(image_width, image_height, point_x, point_y, processed_image_width=224,
                     processed_image_height=224):
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

    @staticmethod
    def get_angle(p0, p1=np.array([0, 0]), p2=None):
        """ compute angle (in degrees) for p0p1p2 corner
        Inputs:
            p0,p1,p2 - points in the form of [x,y]
        """
        if p2 is None:
            p2 = p1 + np.array([1, 0])
        v0 = np.array(p0) - np.array(p1)
        v1 = np.array(p2) - np.array(p1)

        angle = np.math.atan2(np.linalg.det([v0, v1]), np.dot(v0, v1))
        return np.degrees(angle)
