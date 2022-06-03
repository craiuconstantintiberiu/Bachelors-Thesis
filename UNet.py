from abc import ABC

import numpy as np

from ImageConversion import convertImage
from Model import Model


class UNet(Model, ABC):
    def predict_keypoints(self, image):
        masks = self.model.predict(convertImage(image))
        return self._find_coordinates_for_prediction(masks)

    def _find_coordinates_for_mask(self, mask):
        hm_sum = np.sum(mask)

        index_map = [j for i in range(224) for j in range(224)]
        index_map = np.reshape(index_map, newshape=(224, 224))

        x_score_map = mask * index_map / hm_sum
        y_score_map = mask * np.transpose(index_map) / hm_sum

        px = np.sum(np.sum(x_score_map, axis=None))
        py = np.sum(np.sum(y_score_map, axis=None))

        return px, py

    def _find_coordinates_for_prediction(self, masks):
        preds = []
        masks_for_every_keypoint = np.reshape(masks, newshape=(224, 224, 4))
        for k in range(masks_for_every_keypoint.shape[-1]):
            xpred, ypred = self._find_coordinates_for_mask(masks_for_every_keypoint[:, :, k])
            preds.append(xpred)
            preds.append(ypred)
        return preds
