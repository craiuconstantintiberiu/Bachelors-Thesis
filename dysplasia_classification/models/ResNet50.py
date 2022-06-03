from abc import ABC

from dysplasia_classification.image_processing.ImageConversion import convertImage
from dysplasia_classification.models.Model import Model


class ResNet50(Model, ABC):
    def predict_keypoints(self, image):
        return self.model.predict(convertImage(image))[0]
