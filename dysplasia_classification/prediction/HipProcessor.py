from dysplasia_classification.app import app
from dysplasia_classification.classification.DysplasiaClassifier import DysplasiaClassifier
from dysplasia_classification.image_processing.ImageAnnotator import ImageAnnotator
from dysplasia_classification.image_processing.ImageUtils import ImageUtils
from dysplasia_classification.prediction.KeypointPredictor import KeypointPredictor


class HipProcessor:
    def __init__(self, keypoint_predictor):
        self.keypoint_predictor = keypoint_predictor

    def process_radiographs(self, img, models, original_file_name):
        hip_infos = []
        for model in models:
            hip_info = self.keypoint_predictor.predict_keypoints(img, model)
            HipProcessor._set_hip_angles(hip_info)
            HipProcessor._set_classification(hip_info)

            new_file_name = HipProcessor._generate_annotated_image_name(original_file_name, model)
            hip_info.file_name = new_file_name
            HipProcessor._save_annotated_image(new_file_name, img, hip_info)

            hip_infos.append(hip_info)

        return hip_infos

    @staticmethod
    def _set_hip_angles(hip_info):
        hip_info.left_hip_angle = ImageUtils.get_angle(hip_info.left_acetabular, hip_info.left_femoral,
                                                       hip_info.right_femoral)
        hip_info.right_hip_angle = ImageUtils.get_angle(hip_info.left_femoral, hip_info.right_femoral,
                                                        hip_info.right_acetabular)

    @staticmethod
    def _set_classification(hip_info):
        hip_info.left_hip_class, hip_info.right_hip_class = DysplasiaClassifier.classify_hip(hip_info)

    @staticmethod
    def _save_annotated_image(new_file_name, img, hip_info):
        ImageAnnotator.annotate_and_save_radiograph(img, app.config['PREDICTIONS_FOLDER'], new_file_name, hip_info)

    @staticmethod
    def _generate_annotated_image_name(original_filename, model):
        return original_filename + '_' + model + ".svg"
