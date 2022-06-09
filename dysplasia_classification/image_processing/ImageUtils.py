import math

import numpy as np


class ImageUtils:
    @staticmethod
    def get_angle(p0, p1, p2):
        '''
        Computes p0p1p2 angle
        :param p0: coordinates for first point, in form [x,y]
        :param p1: coordinates for second point, in form [x,y]
        :param p2: coordinates for third point, in form [x,y]
        :return: angle, in degrees
        '''
        diff1 = np.array(p0) - np.array(p1)
        mod1 = math.sqrt(diff1[0] * diff1[0] + diff1[1] * diff1[1])

        diff2 = np.array(p2) - np.array(p1)
        mod2 = math.sqrt(diff2[0] * diff2[0] + diff2[1] * diff2[1])

        ratio = (diff1[0]*diff2[0]+diff1[1]*diff1[1])/(mod1*mod2)

        return round(np.degrees(math.acos(ratio)), 2)

    @staticmethod
    def scale_point(new_width, new_height, coordinates, original_width=224,
                    original_height=224):
        """
        :param new_width: Width of initial resized_and_converted_image
        :param new_height: Height of initial image
        :param original_width: Width of processed image
        :param original_height: Height of processed image
        :param coordinates: (X,Y) coordinates of point
        :return: The corresponding (x,y) of the point if it were to be situated in the same place, but on the other image
        """
        return coordinates[0] * new_width / original_width, coordinates[1] * new_height / original_height
