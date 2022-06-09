from unittest import TestCase
from unittest.mock import patch, ANY

import numpy as np

from dysplasia_classification.classification.DysplasiaGrade import DysplasiaGrade
from dysplasia_classification.hip_information.HipInformation import HipInformation
from dysplasia_classification.models.Model import Model
from dysplasia_classification.prediction.HipProcessor import HipProcessor
from dysplasia_classification.prediction.KeypointPredictor import KeypointPredictor


class TestHipProcessor(TestCase):

    @patch("dysplasia_classification.prediction.HipProcessor.ImageAnnotator")
    @patch("tests.test_HipProcessor.KeypointPredictor")
    def test_integration_whenProcessingRadiograph_thenImageIsAnnotatedAndSaved_andReturnValueIsCorrect(self, predictor,
                                                                                                       annotator):
        img = np.zeros((224, 224))
        processor = HipProcessor(predictor)
        file_name = "radiograph"

        hip_info = HipInformation((1, 1), (2, 2), (3, 3), (4, 4), "model")
        predictor.predict_keypoints.return_value = hip_info

        hip_infos = processor.process_radiograph(img, ["model"], file_name)

        annotator.annotate_and_save_radiograph.assert_called_once_with(img, ANY, "radiograph_model.svg", hip_info)

        first_hip_info = hip_infos[0]
        self.assertEqual(first_hip_info.left_acetabular, hip_info.left_acetabular)
        self.assertEqual(first_hip_info.left_femoral, hip_info.left_femoral)
        self.assertEqual(first_hip_info.right_femoral, hip_info.right_femoral)
        self.assertEqual(first_hip_info.right_acetabular, hip_info.right_acetabular)
        self.assertEqual(first_hip_info.model, hip_info.model)


class SimpleKeypointPredictor(KeypointPredictor):
    def __init__(self):
        self._model_dict = {}


class SimpleModel(Model):
    def __init__(self):
        pass
