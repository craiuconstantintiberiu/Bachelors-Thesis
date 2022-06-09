from abc import ABC

import keras
import numpy as np
from keras import Input
from keras.layers import Conv2D, MaxPooling2D, Conv2DTranspose, Reshape, concatenate

from dysplasia_classification.models.Model import Model


class UNet(Model, ABC):
    def predict_keypoints(self, image):
        masks = self.model.predict(Model._process_image(image))
        return self.__find_coordinates_for_prediction(masks)

    def __find_coordinates_for_mask(self, mask):
        summ = np.sum(mask)
        positions = np.zeros((224, 224))
        for i in range(224):
            for j in range(224):
                positions[i][j] = j
        x_score_map = mask * positions / summ
        y_score_map = mask * np.transpose(positions) / summ
        keypoint_x = np.sum(x_score_map, axis=None)
        keypoint_y = np.sum(y_score_map, axis=None)
        return keypoint_x, keypoint_y

    def __find_coordinates_for_prediction(self, masks):
        preds = []
        masks_for_every_keypoint = np.reshape(masks, newshape=(224, 224, 4))
        for k in range(masks_for_every_keypoint.shape[-1]):
            xpred, ypred = self.__find_coordinates_for_mask(masks_for_every_keypoint[:, :, k])
            preds.append(xpred)
            preds.append(ypred)
        return preds

    def create_model(self):

        input = Input((224,224,1), name="Input")

        # contract
        x = Conv2D(64, kernel_size=(3, 3), strides=1, padding='same', activation='relu',
                   name="Block{0}_Conv1".format(str(1)))(input)
        x = Conv2D(64, kernel_size=(3, 3), strides=1, padding='same', activation='relu',
                   name="Block" + str(1) + "_Conv2")(x)
        skip1 = x
        x = MaxPooling2D(pool_size=(2, 2), strides=2, padding='valid',
                         name="Block" + str(1) + "_Pool1")(x)


        x = Conv2D(128, kernel_size=(3, 3), strides=1, padding='same', activation='relu',
                   name="Block" + str(2) + "_Conv1")(x)
        x = Conv2D(128, kernel_size=(3, 3), strides=1, padding='same', activation='relu',
                   name="Block" + str(2) + "_Conv2")(x)
        skip2 = x
    
        x = MaxPooling2D(pool_size=(2, 2), strides=2, padding='valid',
                         name="Block" + str(2) + "_Pool1")(x)

        x = Conv2D(256, kernel_size=(3, 3), strides=1, padding='same', activation='relu',
                   name="Block" + str(3) + "_Conv1")(x)
        x = Conv2D(256, kernel_size=(3, 3), strides=1, padding='same', activation='relu',
                   name="Block" + str(3) + "_Conv2")(x)
        skip3 = x

        x = MaxPooling2D(pool_size=(2, 2), strides=2, padding='valid',
                         name="Block" + str(3) + "_Pool1")(x)

        x = Conv2D(512, kernel_size=(3, 3), strides=1, padding='same', activation='relu',
                   name="Block" + str(4) + "_Conv1")(x)
        x = Conv2D(512, kernel_size=(3, 3), strides=1, padding='same', activation='relu',
                   name="Block" + str(4) + "_Conv2")(x)
        skip4 = x

        x = MaxPooling2D(pool_size=(2, 2), strides=2, padding='valid',
                             name="Block" + str(4) + "_Pool1")(x)

        x = Conv2D(1024, kernel_size=(3, 3), strides=1, padding='same', activation='relu',
                   name="Block" + str(5) + "_Conv1")(x)
        x = Conv2D(1024, kernel_size=(3, 3), strides=1, padding='same', activation='relu',
                   name="Block" + str(5) + "_Conv2")(x)


        #expand
        x = Conv2DTranspose(512, kernel_size=(2, 2), strides=2, padding='valid', activation='relu',
                            name="Block" + str(6) + "_ConvT1")(x)
        x = concatenate([x, skip4], axis=-1, name="Block" + str(6) + "_Concat1")
        x = Conv2D(512, kernel_size=(3, 3), strides=1, padding='same', activation='relu',
                   name="Block" + str(6) + "_Conv1")(x)
        x = Conv2D(512, kernel_size=(3, 3), strides=1, padding='same', activation='relu',
                   name="Block" + str(6) + "_Conv2")(x)

        x = Conv2DTranspose(256, kernel_size=(2, 2), strides=2, padding='valid', activation='relu',
                            name="Block" + str(7) + "_ConvT1")(x)
        x = concatenate([x, skip3], axis=-1, name="Block" + str(7) + "_Concat1")
        x = Conv2D(256, kernel_size=(3, 3), strides=1, padding='same', activation='relu',
                   name="Block" + str(7) + "_Conv1")(x)
        x = Conv2D(256, kernel_size=(3, 3), strides=1, padding='same', activation='relu',
                   name="Block" + str(7) + "_Conv2")(x)

        x = Conv2DTranspose(128, kernel_size=(2, 2), strides=2, padding='valid', activation='relu',
                            name="Block" + str(8) + "_ConvT1")(x)
        x = concatenate([x, skip2], axis=-1, name="Block" + str(8) + "_Concat1")
        x = Conv2D(128, kernel_size=(3, 3), strides=1, padding='same', activation='relu',
                   name="Block" + str(8) + "_Conv1")(x)
        x = Conv2D(128, kernel_size=(3, 3), strides=1, padding='same', activation='relu',
                   name="Block" + str(8) + "_Conv2")(x)

        x = Conv2DTranspose(64, kernel_size=(2, 2), strides=2, padding='valid', activation='relu',
                            name="Block" + str(9) + "_ConvT1")(x)
        x = concatenate([x, skip1], axis=-1, name="Block" + str(9) + "_Concat1")
        x = Conv2D(64, kernel_size=(3, 3), strides=1, padding='same', activation='relu',
                   name="Block" + str(9) + "_Conv1")(x)
        x = Conv2D(64, kernel_size=(3, 3), strides=1, padding='same', activation='relu',
                   name="Block" + str(9) + "_Conv2")(x)

        output = Conv2D(4, kernel_size=(1, 1), strides=1, padding='valid', activation='linear', name="output")(x)
        output = Reshape(target_shape=(224 * 224 * 4, 1))(output)

        model = keras.Model(inputs=input, outputs=output, name="Output")

        return model



