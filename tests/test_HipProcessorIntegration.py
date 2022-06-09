from unittest import TestCase
from unittest.mock import patch, ANY

import numpy as np

from dysplasia_classification.classification.DysplasiaGrade import DysplasiaGrade
from dysplasia_classification.hip_information.HipInformation import HipInformation
from dysplasia_classification.models.Model import Model
from dysplasia_classification.prediction.HipProcessor import HipProcessor
from dysplasia_classification.prediction.KeypointPredictor import KeypointPredictor


class TestHipProcessorIntegration(TestCase):

    def test_integration_whenProcessingRadiograph_thenRadiographsAreProcessedAndHipInfosAreSet(self):
        img = (255.0 * np.random.random((224, 224, 3))).astype(np.uint8)

        keypoint_predictor = KeypointPredictor()
        processor = HipProcessor(keypoint_predictor)
        file_name = "radiograph"

        hip_infos = processor.process_radiograph(img, ["ResNet", "U-Net"], file_name)
        print(hip_infos)

        self.assertEqual(hip_infos[0].model, "ResNet")
        self.assertNotEqual(hip_infos[0].left_hip_class, "")
        self.assertNotEqual(hip_infos[0].right_hip_class, "")
        self.assertEqual(hip_infos[1].model, "U-Net")
        self.assertNotEqual(hip_infos[1].left_hip_class, "")
        self.assertNotEqual(hip_infos[1].right_hip_class, "")