from dysplasia_classification.models.ResNet50 import ResNet50
from dysplasia_classification.models.UNet import UNet

class KeypointPredictor:
    def __init__(self):
        self._resnet = ResNet50("./FinalResNetModel3June")
        self._unet = UNet("./FinalUNetModel3June")
        self._model_dict = {"ResNet": self._resnet, "U-Net": self._unet}

    def predict_keypoints(self, image, models=None):
        if models is None:
            models = ["ResNet"]
        predictions = []
        for model in models:
            keypoints = self._model_dict[model].predict_keypoints(image)
            predictions.append(keypoints)
        return predictions
