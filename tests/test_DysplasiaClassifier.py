from unittest import TestCase

from dysplasia_classification.classification.DysplasiaClassifier import DysplasiaClassifier
from dysplasia_classification.classification.DysplasiaGrade import DysplasiaGrade
from dysplasia_classification.hip_information.HipInformation import HipInformation


def create_hip_info(left_hip_angle, right_hip_angle):
    hip_info = HipInformation(1, 1, 1, 1, 1)
    hip_info.left_hip_angle, hip_info.right_hip_angle = left_hip_angle, right_hip_angle
    return hip_info


class TestDysplasiaClassifier(TestCase):
    def test_given89Degrees_thenReturnGradeE(self):
        hip_info = create_hip_info(89, 89)
        self.assertEqual(DysplasiaClassifier.classify_hip(hip_info), (DysplasiaGrade.E, DysplasiaGrade.E))

    def test_given90Degrees_thenReturnGradeCD(self):
        hip_info = create_hip_info(90, 90)
        self.assertEqual(DysplasiaClassifier.classify_hip(hip_info), (DysplasiaGrade.CD, DysplasiaGrade.CD))

    def test_given91Degrees_thenReturnGradeCD(self):
        hip_info = create_hip_info(91, 91)
        self.assertEqual(DysplasiaClassifier.classify_hip(hip_info), (DysplasiaGrade.CD, DysplasiaGrade.CD))

    def test_given99Degrees_thenReturnGradeCD(self):
        hip_info = create_hip_info(99, 99)
        self.assertEqual(DysplasiaClassifier.classify_hip(hip_info), (DysplasiaGrade.CD, DysplasiaGrade.CD))

    def test_given100Degrees_thenReturnGradeAB(self):
        hip_info = create_hip_info(100, 100)
        self.assertEqual(DysplasiaClassifier.classify_hip(hip_info), (DysplasiaGrade.AB, DysplasiaGrade.AB))

    def test_given101Degrees_thenReturnGradeAB(self):
        hip_info = create_hip_info(101, 101)
        self.assertEqual(DysplasiaClassifier.classify_hip(hip_info), (DysplasiaGrade.AB, DysplasiaGrade.AB))

    def test_given80And104Degrees_thenReturnGradeEAndAb(self):
        hip_info = create_hip_info(80, 104)
        self.assertEqual(DysplasiaClassifier.classify_hip(hip_info), (DysplasiaGrade.E, DysplasiaGrade.AB))
