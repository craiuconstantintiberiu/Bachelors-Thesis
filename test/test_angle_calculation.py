import unittest
from MLPart import scale_points, scale_x_and_y_values
import numpy as np

class TestPointScaling(unittest.TestCase):
    def test_point_scaling_image_is_double(self):
        self.assertEqual((256, 256), scale_points(1024, 1024, 128, 128, 512, 512))

    def test_point_scaling_image_is_half(self):
        self.assertEqual((64, 64), scale_points(256, 256, 128, 128, 512, 512))

    def test_scale_x_and_y_values_should_be_double(self):
        height=1024
        width=1024
        x_values=np.array([10,20,30,40])
        y_values=np.array([10,20,30,40])
        self.assertEqual(scale_x_and_y_values(width,height,x_values,y_values), ([20,40,60,80],[20,40,60,80]))


if __name__ == '__main__':
    unittest.main()
