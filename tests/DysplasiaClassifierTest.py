import unittest
from dysplasia_classification.classification.DysplasiaGrade import classify_based_on_angle, Dysplasia


class MyTestCase(unittest.TestCase):
    def testEClass(self):
        self.assertEqual(classify_based_on_angle(87), Dysplasia.E)

    def testDClass(self):
        self.assertEqual(classify_based_on_angle(95), Dysplasia.D)

    def testCClass(self):
        self.assertEqual(classify_based_on_angle(100), Dysplasia.C)

    def testBClass(self):
        self.assertEqual(classify_based_on_angle(103), Dysplasia.B)

    def testAClass(self):
        self.assertEqual(classify_based_on_angle(110), Dysplasia.A)


if __name__ == '__main__':
    unittest.main()
