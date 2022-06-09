from unittest import TestCase
from unittest.mock import patch

import numpy as np
from werkzeug.datastructures import FileStorage

from dysplasia_classification.UI import show_hip_information_and_annotated_radiographs
from dysplasia_classification.app import app
from dysplasia_classification.classification.DysplasiaGrade import DysplasiaGrade
from dysplasia_classification.hip_information.HipInformation import HipInformation
from dysplasia_classification.models.Model import Model
from dysplasia_classification.prediction.KeypointPredictor import KeypointPredictor


class TestUI(TestCase):

    @patch("dysplasia_classification.UI.get_chosen_models")
    @patch("flask.templating.render_template")
    @patch("dysplasia_classification.UI.processor")
    @patch("werkzeug.datastructures.FileStorage")
    @patch("cv2.imread")
    def test_afterRadiographIsProcessed_thenUploadPageIsShownAgain(self, imread, file, processor,
                                                                   render_template, chosen_models):
        img = np.zeros((224, 224))
        file.filename = "radiograph.png"
        imread.return_value = img
        chosen_models.return_value = []

        with app.test_request_context():
            radiographs = show_hip_information_and_annotated_radiographs(file)
            self.assertTrue(radiographs.__contains__(
                "Select models to be used in predicting the Norberg Angles:"))

    @patch("dysplasia_classification.UI.get_chosen_models")
    @patch("flask.templating.render_template")
    @patch("dysplasia_classification.UI.processor")
    @patch("werkzeug.datastructures.FileStorage")
    @patch("cv2.imread")
    def test_afterRadiographIsProcessed_thenAnnotatedRadiographAreShown(self, imread, file, processor,
                                                                        render_template, chosen_models):
        img = np.zeros((224, 224))
        hipInformation1 = HipInformation((1, 1), (2, 2), (3, 3), (4, 4), "ResNet")
        hipInformation1.left_hip_angle = 90
        hipInformation1.right_hip_angle = 100
        hipInformation1.left_hip_class = DysplasiaGrade.CD
        hipInformation1.right_hip_class = DysplasiaGrade.CD
        hipInformation1.file_name = "hip1.png"

        hipInformation2 = HipInformation((1, 1), (2, 2), (3, 3), (4, 4), "U-Net")
        hipInformation2.left_hip_angle = 120
        hipInformation2.right_hip_angle = 130
        hipInformation2.left_hip_class = DysplasiaGrade.AB
        hipInformation2.right_hip_class = DysplasiaGrade.AB
        hipInformation2.file_name = "hip2.png"

        file.filename = "radiograph.png"
        imread.return_value = img
        processor.process_radiograph.return_value = [hipInformation1, hipInformation2]
        chosen_models.return_value = ["ResNet", "U-Net"]

        with app.test_request_context():
            radiographs = show_hip_information_and_annotated_radiographs(file)
            processor.process_radiograph.assert_called_once_with(img, ["ResNet", "U-Net"], "radiograph.png")

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