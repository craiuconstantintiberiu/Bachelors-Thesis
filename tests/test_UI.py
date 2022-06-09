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


class TestUI(TestCase):
    #
    # @patch("dysplasia_classification.UI.predictor")
    # @patch("dysplasia_classification.UI.processor")
    # @patch("dysplasia_classification.UI.render_template")
    # @patch("dysplasia_classification.UI.get_chosen_models")
    @patch("flask.templating.render_template")
    @patch("dysplasia_classification.UI.flask.globals.request")
    @patch("dysplasia_classification.UI.processor")
    @patch("dysplasia_classification.UI")
    @patch("werkzeug.datastructures.FileStorage")
    @patch("cv2.imread")
    def test_afterRadiographIsProcessed_thenUploadPageIsShownAgain(self, imread, file, ui, processor, request,
                                                                   render_template):
        img = np.zeros((224, 224))
        file.filename = "radiograph.png"
        imread.return_value = img

        with app.test_request_context():
            self.assertTrue(return_hip_information_and_annotated_radiographs(file).__contains__(
                "Select models to be used in predicting the Norberg Angles:"))

    @patch("flask.templating.render_template")
    @patch("dysplasia_classification.UI.flask.globals.request")
    @patch("dysplasia_classification.UI.processor")
    @patch("dysplasia_classification.UI")
    @patch("werkzeug.datastructures.FileStorage")
    @patch("cv2.imread")
    def test_afterRadiographIsProcessed_thenAnnotatedRadiographIsShown(self, imread, file, ui, processor, request,
                                                                       render_template):
        img = np.zeros((224, 224))
        hipInformation1 = HipInformation((1, 1), (2, 2), (3, 3), (4, 4), "ResNet")
        hipInformation1.left_hip_angle = 90
        hipInformation1.right_hip_angle = 100
        hipInformation1.left_hip_class = DysplasiaGrade.CD
        hipInformation1.right_hip_class = DysplasiaGrade.CD
        hipInformation1.file_name = "ASDSA"
        file.filename = "radiograph.png"
        imread.return_value = img
        processor.process_radiograph.return_value = [hipInformation1]
        with app.test_request_context():
            radiographs = return_hip_information_and_annotated_radiographs(file)
            print(radiographs)
            self.assertTrue(radiographs.__contains__("Select models to be used in predicting the Norberg Angles:"))
            # processor.process_radiograph.assert_called_once()


class SimpleModel(Model):
    def __init__(self):
        pass


class SimpleFileStorage(FileStorage):
    def __init__(self):
        self.filename = "radiograph.png"
