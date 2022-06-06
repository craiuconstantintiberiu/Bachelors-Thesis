from abc import abstractmethod

import numpy as np
from keras.models import load_model


class Model:
    def __init__(self, location):
        self.model = load_model(location,compile=False)
        self._warm_up_model()

    def _warm_up_model(self):
        for _ in range(5):
            self.model.predict(np.array([np.zeros((224, 224, 1))]))
            self.model.predict(np.array([np.zeros((224, 224, 1))]))
            self.model.predict(np.array([np.zeros((224, 224, 1))]))
            self.model.predict(np.array([np.zeros((224, 224, 1))]))
            self.model.predict(np.array([np.zeros((224, 224, 1))]))

    @abstractmethod
    def predict_keypoints(self, image):
        pass
