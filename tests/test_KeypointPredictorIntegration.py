from unittest import TestCase

import numpy as np

from dysplasia_classification.prediction.KeypointPredictor import KeypointPredictor


class TestKeypointPredictor(TestCase):

    def test_whenPredictingKeypoints_thenCorrectHipInformationIsCreated(self):
        predictor = KeypointPredictor()
        img = (255.0 * np.random.random((224, 224, 3))).astype(np.uint8)

        hip_info_0 = predictor.predict_keypoints(img, "ResNet")
        hip_info_1 = predictor.predict_keypoints(img, "U-Net")

        self.assertEqual(hip_info_0.model, "ResNet")
        self.assertEqual(hip_info_1.model, "U-Net")
