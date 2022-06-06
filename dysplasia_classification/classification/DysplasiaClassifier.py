from dysplasia_classification.classification.DysplasiaGrade import DysplasiaGrade


class DysplasiaClassifier:
    @staticmethod
    def classify_based_on_angle(angle):
        if angle < 90:
            return DysplasiaGrade.AB
        if angle < 100:
            return DysplasiaGrade.CD
        return DysplasiaGrade.E
