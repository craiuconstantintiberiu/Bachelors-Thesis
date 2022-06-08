from copy import copy

from matplotlib import pyplot as plt

from .ImageUtils import ImageUtils
from ..image_processing.AngleAnnotation import AngleAnnotation


class ImageAnnotator:
    @staticmethod
    def annotate_and_save_radiograph(image, folder, new_image_name, hip_info):
        width, height = image.shape[1], image.shape[0]

        scaled_hip_info = copy(hip_info)
        scaled_hip_info.left_acetabular = ImageUtils.scale_point(width, height, scaled_hip_info.left_acetabular)
        scaled_hip_info.left_femoral = ImageUtils.scale_point(width, height, scaled_hip_info.left_femoral)
        scaled_hip_info.right_femoral = ImageUtils.scale_point(width, height, scaled_hip_info.right_femoral)
        scaled_hip_info.right_acetabular = ImageUtils.scale_point(width, height, scaled_hip_info.right_acetabular)

        fig, axis = plt.subplots()
        plt.imshow(image)
        ImageAnnotator.plot_line_between_two_points(scaled_hip_info.left_acetabular,
                                                    scaled_hip_info.left_femoral)
        ImageAnnotator.plot_line_between_two_points(scaled_hip_info.left_femoral,
                                                    scaled_hip_info.right_femoral)
        ImageAnnotator.plot_line_between_two_points(scaled_hip_info.right_femoral,
                                                    scaled_hip_info.right_acetabular)

        ImageAnnotator.plot_arc_for_angle(axis, scaled_hip_info.left_hip_angle, scaled_hip_info.left_acetabular,
                                          scaled_hip_info.left_femoral, scaled_hip_info.right_femoral)
        ImageAnnotator.plot_arc_for_angle(axis, scaled_hip_info.right_hip_angle, scaled_hip_info.left_femoral,
                                          scaled_hip_info.right_femoral, scaled_hip_info.right_acetabular)

        plt.axis("off")
        plt.savefig(folder + new_image_name, bbox_inches='tight', pad_inches=0)
        plt.close()
        plt.show()

    @staticmethod
    def plot_arc_for_angle(axis, angle, point1, point2, point3):
        AngleAnnotation(point2, (point3[0], point3[1]),
                        (point1[0], point1[1]), ax=axis, size=20, text=str(angle),
                        textposition="inside",
                        text_kw=dict(fontsize=3, color="blue"))

    @staticmethod
    def plot_line_between_two_points(point1, point2):
        plt.plot([point1[0], point2[0]], [point1[1], point2[1]], 'r-', linewidth=0.6)
