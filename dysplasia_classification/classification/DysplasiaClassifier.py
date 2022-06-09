from dysplasia_classification.classification.DysplasiaGrade import DysplasiaGrade


class DysplasiaClassifier:
    @staticmethod
    def __classify_based_on_angle(angle):
        if angle < 90:
            return DysplasiaGrade.E
        if angle < 100:
            return DysplasiaGrade.CD
        return DysplasiaGrade.AB

    @staticmethod
    def classify_hip(hip_information):
        '''
        Classifies the left and right hips for canine dysplasia
        :param hip_information: HipInformation object, with values set for left and right Norberg angles
        :return: a tuple (left_hip_class, right_hip_class) representing the left and right Hip Dysplasia classes
        '''
        return DysplasiaClassifier.__classify_based_on_angle(
            hip_information.left_hip_angle), DysplasiaClassifier.__classify_based_on_angle(
            hip_information.right_hip_angle)
