from unittest import TestCase
from unittest.mock import patch, ANY

import numpy as np
from werkzeug.datastructures import FileStorage, ImmutableMultiDict

import dysplasia_classification.UI
from dysplasia_classification.UI import return_hip_information_and_annotated_radiographs
from dysplasia_classification.app import app
from dysplasia_classification.classification.DysplasiaGrade import DysplasiaGrade
from dysplasia_classification.hip_information.HipInformation import HipInformation
from dysplasia_classification.models.Model import Model
from dysplasia_classification.prediction.HipProcessor import HipProcessor
from dysplasia_classification.prediction.KeypointPredictor import KeypointPredictor


class SimpleKeypointPredictor(KeypointPredictor):
    def __init__(self):
        self._model_dict = {}


class TestUIIntegration(TestCase):

    @patch("dysplasia_classification.image_processing.ImageAnnotator")
    @patch("tests.test_UIIntegration.SimpleModel")
    @patch("dysplasia_classification.UI.get_chosen_models")
    @patch("flask.templating.render_template")
    @patch("dysplasia_classification.prediction.HipProcessor.HipProcessor")
    @patch("dysplasia_classification.UI.processor")
    @patch("werkzeug.datastructures.FileStorage")
    @patch("cv2.imread")
    def test_afterRadiographIsProcessed_thenAnnotatedRadiographAreShown(self, imread, file, processor, hp,
                                                                        render_template, chosen_models, model,
                                                                        annotator):
        img = np.zeros((224, 224))

        file.filename = "radiograph.png"
        imread.return_value = img

        keypoint_predictor = SimpleKeypointPredictor()
        keypoint_predictor._model_dict = {"model": SimpleModel()}
        processor.keypoint_predictor = keypoint_predictor
        chosen_models.return_value = ["model"]

        with app.test_request_context():
            radiographs = return_hip_information_and_annotated_radiographs(file)
            print(radiographs)
            processor.process_radiograph.assert_called_once_with(img, ["model"], "radiograph.png")

            self.assertTrue(radiographs.__contains__("Prediction for ResNet"))
            self.assertTrue(radiographs.__contains__("<img src=\"/display/../static/predictions/hip1.png\">"))
            self.assertTrue(radiographs.__contains__(
                "The Norberg Angle for the left hip is 90, resulting in a class C-D classification."))
            self.assertTrue(radiographs.__contains__(
                "The Norberg Angle for the right hip is 100, resulting in a class C-D classification."))

            self.assertTrue(radiographs.__contains__("Prediction for U-Net"))
            self.assertTrue(radiographs.__contains__("<img src=\"/display/../static/predictions/hip2.png\">"))

            self.assertTrue(radiographs.__contains__(
                "The Norberg Angle for the left hip is 120, resulting in a class A-B classification."))
            self.assertTrue(radiographs.__contains__(
                "The Norberg Angle for the right hip is 130, resulting in a class A-B classification."))


class SimpleKeypointPredictor(KeypointPredictor):
    def __init__(self):
        self._model_dict = {}


class SimpleModel(Model):
    def __init__(self):
        pass


class SimpleFileStorage(FileStorage):
    def __init__(self):
        self.filename = "radiograph.png"
