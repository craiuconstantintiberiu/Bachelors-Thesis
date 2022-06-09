from unittest import TestCase
from unittest.mock import patch

import numpy as np

from dysplasia_classification.hip_information.HipInformation import HipInformation
from dysplasia_classification.models.Model import Model
from dysplasia_classification.prediction.KeypointPredictor import KeypointPredictor


class TestKeypointPredictor(TestCase):

    @patch("tests.test_KeypointPredictor.SimpleModel")
    def test_whenPredictingKeypoints_thenCorrectHipInformationIsCreated(self, model):
        predictor = SimpleKeypointPredictor()
        predictor._model_dict = {"model": model}

        model.predict_keypoints.return_value = np.array([1, 2, 3, 4, 5, 6, 7, 8])
        pred = predictor.predict_keypoints(np.zeros((224, 224)), "model")

        expected_hip_information = HipInformation((1, 2), (3, 4), (5, 6), (7, 8), "model")

        self.assertEqual(pred.left_acetabular, expected_hip_information.left_acetabular)
        self.assertEqual(pred.left_femoral, expected_hip_information.left_femoral)
        self.assertEqual(pred.right_femoral, expected_hip_information.right_femoral)
        self.assertEqual(pred.right_acetabular, expected_hip_information.right_acetabular)
        self.assertEqual(pred.model, expected_hip_information.model)

    @patch("tests.test_KeypointPredictor.SimpleModel")
    def test_whenPredictingKeypoints_thenCallToModelIsMade(self, model):
        predictor = SimpleKeypointPredictor()
        predictor._model_dict = {"model": model}
        model.predict_keypoints.return_value = np.array([1, 2, 3, 4, 5, 6, 7, 8])
        predictor.predict_keypoints(np.zeros((224, 224)), "model")
        model.predict_keypoints.assert_called_once()


class SimpleKeypointPredictor(KeypointPredictor):
    def __init__(self):
        self._model_dict = {}


class SimpleModel(Model):
    def __init__(self):
        pass
