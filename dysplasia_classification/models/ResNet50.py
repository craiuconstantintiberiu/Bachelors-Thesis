from abc import ABC

from dysplasia_classification.models.Model import Model


class ResNet50(Model, ABC):
    def predict_keypoints(self, image):
        return self.model.predict(Model._process_image(image))[0]
