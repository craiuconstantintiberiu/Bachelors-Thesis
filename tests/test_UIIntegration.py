from unittest import TestCase
from unittest.mock import patch

import numpy as np

from dysplasia_classification.UI import show_hip_information_and_annotated_radiographs, processor
from dysplasia_classification.app import app
from dysplasia_classification.prediction.KeypointPredictor import KeypointPredictor


class SimpleKeypointPredictor(KeypointPredictor):
    def __init__(self):
        self._model_dict = {}


class TestUIIntegration(TestCase):

    @patch("dysplasia_classification.image_processing.ImageAnnotator")
    @patch("dysplasia_classification.UI.get_chosen_models")
    @patch("flask.templating.render_template")
    @patch("werkzeug.datastructures.FileStorage")
    @patch("cv2.imread")
    def test_afterRadiographIsProcessed_thenAnnotatedRadiographAreShown(self, imread, file,
                                                                        render_template, chosen_models,
                                                                        annotator):
        img = (255.0 * np.random.random((224, 224, 3))).astype(np.uint8)

        file.filename = "radiograph.png"
        imread.return_value = img

        keypoint_predictor = KeypointPredictor()
        processor.keypoint_predictor = keypoint_predictor
        chosen_models.return_value = ["ResNet", "U-Net"]

        with app.test_request_context():
            radiographs = show_hip_information_and_annotated_radiographs(file)
            print(radiographs)
            self.assertTrue(radiographs.__contains__("Prediction for ResNet"))
            self.assertTrue(radiographs.__contains__("Prediction for U-Net"))
