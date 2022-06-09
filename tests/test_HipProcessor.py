from unittest import TestCase
from unittest.mock import patch, ANY

import numpy as np

from dysplasia_classification.classification.DysplasiaGrade import DysplasiaGrade
from dysplasia_classification.hip_information.HipInformation import HipInformation
from dysplasia_classification.models.Model import Model
from dysplasia_classification.prediction.HipProcessor import HipProcessor
from dysplasia_classification.prediction.KeypointPredictor import KeypointPredictor


class TestHipProcessor(TestCase):

    @patch("dysplasia_classification.prediction.HipProcessor.DysplasiaClassifier")
    @patch("dysplasia_classification.prediction.HipProcessor.ImageUtils")
    @patch("dysplasia_classification.prediction.HipProcessor.ImageAnnotator")
    @patch("tests.test_HipProcessor.KeypointPredictor")
    def test_whenProcessingRadiograph_thenImageIsAnnotatedAndSavedWithCorrectParameters(self, predictor, annotator,
                                                                                        utils, classifier):
        img = np.zeros((224, 224))
        processor = HipProcessor(predictor)
        file_name = "radiograph"

        utils.get_angle.return_value = 90
        classifier.classify_hip.return_value = DysplasiaGrade.CD, DysplasiaGrade.AB
        hip_info = HipInformation((1, 1), (2, 2), (3, 3), (4, 4), "model")
        predictor.predict_keypoints.return_value = hip_info

        processor.process_radiograph(img, ["model"], file_name)

        annotator.annotate_and_save_radiograph.assert_called_once_with(img, ANY, "radiograph_model.svg", hip_info)

    @patch("dysplasia_classification.prediction.HipProcessor.DysplasiaClassifier")
    @patch("dysplasia_classification.prediction.HipProcessor.ImageUtils")
    @patch("dysplasia_classification.prediction.HipProcessor.ImageAnnotator")
    @patch("tests.test_HipProcessor.KeypointPredictor")
    def test_whenProcessingRadiographWith2Models_then2SetOfHipsAreClassified(self, predictor, annotator,
                                                                             utils, classifier):
        img = np.zeros((224, 224))
        processor = HipProcessor(predictor)
        file_name = "radiograph"

        utils.get_angle.return_value = 90
        classifier.classify_hip.return_value = DysplasiaGrade.CD, DysplasiaGrade.AB
        hip_info = HipInformation((1, 1), (2, 2), (3, 3), (4, 4), "model")
        predictor.predict_keypoints.return_value = hip_info

        processor.process_radiograph(img, ["model", "another_model"], file_name)

        self.assertEqual(classifier.classify_hip.call_count, 2)

    @patch("dysplasia_classification.prediction.HipProcessor.DysplasiaClassifier")
    @patch("dysplasia_classification.prediction.HipProcessor.ImageUtils")
    @patch("dysplasia_classification.prediction.HipProcessor.ImageAnnotator")
    @patch("tests.test_HipProcessor.KeypointPredictor")
    def test_whenProcessingRadiographWith2Models_then2SetsOfKeypointsPredicted(self, predictor, annotator,
                                                                               utils, classifier):
        img = np.zeros((224, 224))
        processor = HipProcessor(predictor)
        file_name = "radiograph"

        utils.get_angle.return_value = 90
        classifier.classify_hip.return_value = DysplasiaGrade.CD, DysplasiaGrade.AB
        hip_info = HipInformation((1, 1), (2, 2), (3, 3), (4, 4), "model")
        predictor.predict_keypoints.return_value = hip_info

        hip_infos = processor.process_radiograph(img, ["model", "another_model"], file_name)

        self.assertEqual(len(hip_infos), 2)
        self.assertEqual(predictor.predict_keypoints.call_count, 2)
        predictor.predict_keypoints.assert_any_call(img, "model")
        predictor.predict_keypoints.assert_any_call(img, "another_model")

    @patch("dysplasia_classification.prediction.HipProcessor.DysplasiaClassifier")
    @patch("dysplasia_classification.prediction.HipProcessor.ImageUtils")
    @patch("dysplasia_classification.prediction.HipProcessor.ImageAnnotator")
    @patch("tests.test_HipProcessor.KeypointPredictor")
    def test_whenProcessingRadiograph_thenCorrectHipInformationIsReturned(self, predictor, annotator,
                                                                          utils, classifier):
        img = np.zeros((224, 224))
        processor = HipProcessor(predictor)
        file_name = "radiograph"

        utils.get_angle.return_value = 90
        classifier.classify_hip.return_value = DysplasiaGrade.CD, DysplasiaGrade.AB
        hip_info = HipInformation((1, 1), (2, 2), (3, 3), (4, 4), "model")
        predictor.predict_keypoints.return_value = hip_info

        hip_infos = processor.process_radiograph(img, ["model", "another_model"], file_name)

        self.assertEqual(len(hip_infos), 2)
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
