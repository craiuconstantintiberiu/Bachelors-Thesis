from abc import ABC

import numpy as np

from dysplasia_classification.models.Model import Model


class UNet(Model, ABC):
    def predict_keypoints(self, image):
        masks = self.model.predict(Model._process_image(image))
        return self._find_coordinates_for_prediction(masks)

    def _find_coordinates_for_mask(self, mask):
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

    def _find_coordinates_for_prediction(self, masks):
        preds = []
        masks_for_every_keypoint = np.reshape(masks, newshape=(224, 224, 4))
        for k in range(masks_for_every_keypoint.shape[-1]):
            xpred, ypred = self._find_coordinates_for_mask(masks_for_every_keypoint[:, :, k])
            preds.append(xpred)
            preds.append(ypred)
        return preds
