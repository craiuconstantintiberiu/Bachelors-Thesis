from dysplasia_classification.hip_information.HipInformation import HipInformation
from dysplasia_classification.models.ResNet50 import ResNet50
from dysplasia_classification.models.UNet import UNet
import os


class KeypointPredictor:
    def __init__(self):
        self._model_dict = {"ResNet": ResNet50(
            os.path.join(os.path.dirname(__file__), "../model_weights/MorningResNetWeightsStripedMSE.h5")),
                            "U-Net": UNet(os.path.join(os.path.dirname(__file__),
                                                       "../model_weights/unetStripped.h5"))}

    def predict_keypoints(self, image, model):
        '''
        Predicts keypoints for a image using a model
        :param image: Image to predict, as numpy array
        :param model: Model to be used in prediction
        :return: HipInformation object, with values for keypoints set
        '''
        prediction = self._model_dict[model].predict_keypoints(image)
        return KeypointPredictor.__convert_to_HipInformation(prediction, model)

    @staticmethod
    def __convert_to_HipInformation(prediction, model):
        x_values = prediction[0::2]
        y_values = prediction[1::2]
        return HipInformation((x_values[0], y_values[0]), (x_values[1], y_values[1]),
                              (x_values[2], y_values[2]), (x_values[3], y_values[3]),
                              model)
