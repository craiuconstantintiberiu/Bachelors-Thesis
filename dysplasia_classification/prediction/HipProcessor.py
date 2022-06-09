from dysplasia_classification.app import app
from dysplasia_classification.classification.DysplasiaClassifier import DysplasiaClassifier
from dysplasia_classification.image_processing.ImageAnnotator import ImageAnnotator
from dysplasia_classification.image_processing.ImageUtils import ImageUtils


class HipProcessor:
    def __init__(self, keypoint_predictor):
        self.keypoint_predictor = keypoint_predictor

    def process_radiograph(self, img, models, original_file_name):
        '''
        Processes a radiograph, according to the models selected, obtaining keypoint, angle and classification data.
        Saves the annotated radiograph.
        :param img: Radiograph to process, as a numpy array
        :param models: Models to be used in predicting the radiograph, represented as array of strings
        :param original_file_name: Radiograph name, to be used when saving its annotated version
        :return: An array containing objects of type HipInformation, representing radiographs for which predictions have
         been made, all values having been set
        '''
        hip_infos = []
        for model in models:
            hip_info = self.keypoint_predictor.predict_keypoints(img, model)
            HipProcessor.__set_hip_angles(hip_info)
            HipProcessor.__set_classification(hip_info)

            new_file_name = HipProcessor.__generate_annotated_image_name(original_file_name, model)
            hip_info.file_name = new_file_name
            HipProcessor.__save_annotated_image(new_file_name, img, hip_info)

            hip_infos.append(hip_info)

        return hip_infos

    @staticmethod
    def __set_hip_angles(hip_info):
        hip_info.left_hip_angle = ImageUtils.get_angle(hip_info.left_acetabular, hip_info.left_femoral,
                                                       hip_info.right_femoral)
        hip_info.right_hip_angle = ImageUtils.get_angle(hip_info.left_femoral, hip_info.right_femoral,
                                                        hip_info.right_acetabular)

    @staticmethod
    def __set_classification(hip_info):
        hip_info.left_hip_class, hip_info.right_hip_class = DysplasiaClassifier.classify_hip(hip_info)

    @staticmethod
    def __save_annotated_image(new_file_name, img, hip_info):
        ImageAnnotator.annotate_and_save_radiograph(img, app.config['PREDICTIONS_FOLDER'], new_file_name, hip_info)

    @staticmethod
    def __generate_annotated_image_name(original_filename, model):
        return original_filename + '_' + model + ".svg"
