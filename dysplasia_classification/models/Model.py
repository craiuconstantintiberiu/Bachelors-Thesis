from abc import abstractmethod
from keras.models import load_model


class Model:
    def __init__(self, location):
        self.model = load_model(location,compile=False)

    @abstractmethod
    def predict_keypoints(self, image):
        pass
