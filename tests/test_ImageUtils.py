from unittest import TestCase

from dysplasia_classification.image_processing.ImageUtils import ImageUtils


class TestImageUtils(TestCase):
    def test_givenRightAngle_thenGetAngleShouldReturn90Degrees(self):
        self.assertEqual(ImageUtils.get_angle([1, 0], [0, 0], [0, 1]), 90.0)
        self.assertEqual(ImageUtils.get_angle([2, 0], [0, 0], [0, 1]), 90.0)
        self.assertEqual(ImageUtils.get_angle([2, 0], [0, 0], [0, 2]), 90.0)

    def test_givenDoubleImageSize_thenPointsShouldBeScaledByDouble(self):
        self.assertEqual((256, 256), ImageUtils.scale_point(1024, 1024, (128, 128), 512, 512))

    def test_givenHalfImageSize_thenPointsShouldBeScaledByHalf(self):
        self.assertEqual((64, 64), ImageUtils.scale_point(256, 256, (128, 128), 512, 512))
