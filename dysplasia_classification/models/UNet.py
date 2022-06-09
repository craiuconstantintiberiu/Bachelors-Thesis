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
        def downsample_block(x, block_num, n_filters, pooling_on=True):
            x = Conv2D(n_filters, kernel_size=(3, 3), strides=1, padding='same', activation='relu',
                       name="Block" + str(block_num) + "_Conv1")(x)
            x = Conv2D(n_filters, kernel_size=(3, 3), strides=1, padding='same', activation='relu',
                       name="Block" + str(block_num) + "_Conv2")(x)
            skip = x

            if pooling_on is True:
                x = MaxPooling2D(pool_size=(2, 2), strides=2, padding='valid',
                                 name="Block" + str(block_num) + "_Pool1")(x)

            return x, skip

        def upsample_block(x, skip, block_num, n_filters):
            x = Conv2DTranspose(n_filters, kernel_size=(2, 2), strides=2, padding='valid', activation='relu',
                                name="Block" + str(block_num) + "_ConvT1")(x)
            x = concatenate([x, skip], axis=-1, name="Block" + str(block_num) + "_Concat1")
            x = Conv2D(n_filters, kernel_size=(3, 3), strides=1, padding='same', activation='relu',
                       name="Block" + str(block_num) + "_Conv1")(x)
            x = Conv2D(n_filters, kernel_size=(3, 3), strides=1, padding='same', activation='relu',
                       name="Block" + str(block_num) + "_Conv2")(x)

            return x

        input = Input((224,224,1), name="Input")

        # downsampling
        x, skip1 = downsample_block(input, 1, 64)
        x, skip2 = downsample_block(x, 2, 128)
        x, skip3 = downsample_block(x, 3, 256)
        x, skip4 = downsample_block(x, 4, 512)
        x, _ = downsample_block(x, 5, 1024, pooling_on=False)

        # upsampling
        x = upsample_block(x, skip4, 6, 512)
        x = upsample_block(x, skip3, 7, 256)
        x = upsample_block(x, skip2, 8, 128)
        x = upsample_block(x, skip1, 9, 64)

        output = Conv2D(4, kernel_size=(1, 1), strides=1, padding='valid', activation='linear', name="output")(x)
        output = Reshape(target_shape=(224 * 224 * 4, 1))(output)

        model = keras.Model(inputs=input, outputs=output, name="Output")

        return model



