from abc import ABC

from ImageConversion import convertImage
from Model import Model


class ResNet50(Model, ABC):
    def predict_keypoints(self, image):
        return self.model.predict(convertImage(image))[0]
