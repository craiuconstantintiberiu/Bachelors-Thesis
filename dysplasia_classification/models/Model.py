from abc import abstractmethod

import cv2
import numpy as np
from keras.models import load_model


class Model:
    def __init__(self, location):
        self.model = load_model(location,compile=False)
        self._warm_up_model()

    def _warm_up_model(self):
        for _ in range(5):
            self.model.predict(np.array([np.zeros((224, 224, 1))]))

    @staticmethod
    def _process_image(image):
        color = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        resize = cv2.resize(color, dsize=(224, 224), interpolation=cv2.INTER_CUBIC)
        reshape = np.reshape(resize, (224, 224, 1))
        normalized = reshape / 255.0
        return np.array([normalized])

    @abstractmethod
    def predict_keypoints(self, image):
        pass
