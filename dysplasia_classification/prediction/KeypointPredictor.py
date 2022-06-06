import numpy as np
from matplotlib import pyplot as plt

from dysplasia_classification.models.ResNet50 import ResNet50
from dysplasia_classification.models.UNet import UNet

import time


class KeypointPredictor:
    def __init__(self):

        self._resnet = ResNet50("./FinalResNetModel3June")
        self._unet = UNet("./FinalUNetModel3June")
        self._model_dict = {"ResNet": self._resnet, "U-Net": self._unet}

    import time

    start = time.time()
    print("hello")
    end = time.time()
    print(end - start)
    def predict_keypoints(self, image, models=None):
        if models is None:
            models = ["ResNet"]
        predictions = []
        for model in models:
            start = time.time()
            keypoints = self._model_dict[model].predict_keypoints(image)
            end = time.time()
            print("Prediction took "+str(end-start)+" on "+ model)
            predictions.append(keypoints)
        return predictions
