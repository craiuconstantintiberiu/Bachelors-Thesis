from abc import ABC

from keras import Sequential
from keras.layers import Conv2D, LeakyReLU, GlobalAveragePooling2D, Dense, Dropout
from tensorflow import keras

from dysplasia_classification.models.Model import Model


class ResNet50(Model, ABC):
    def predict_keypoints(self, image):
        return self.model.predict(Model._process_image(image))[0]

    def create_model(self):
        model = Sequential()
        pretrained_model = keras.applications.resnet.ResNet50(input_shape=(224, 224, 3), include_top=False,
                                                              weights=None)
        pretrained_model.trainable = True

        model.add(Conv2D(3, (1, 1), padding='same', input_shape=(224, 224, 1)))
        model.add(LeakyReLU(alpha=0.3))
        model.add(pretrained_model)
        model.add(GlobalAveragePooling2D())
        model.add(Dense(256))
        model.add(Dropout(0.3))
        model.add(Dense(8))
        model.summary()
        model.layers[2].trainable = True
        return model
