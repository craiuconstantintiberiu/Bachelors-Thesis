from unittest import TestCase
from unittest.mock import patch, ANY

import numpy as np

from dysplasia_classification.hip_information.HipInformation import HipInformation
from dysplasia_classification.image_processing.ImageAnnotator import ImageAnnotator


class TestImageAnnotator(TestCase):

    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.imshow')
    def test_annotated_radiograph_is_saved_correctly(self, imshow, savefig):
        self.annotate_and_save_radiograph()
        imshow.assert_called_once()
        savefig.assert_called_once_with('folderimg', bbox_inches='tight', pad_inches=0)

    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.plot')
    def test_annotated_radiograph_lines_are_correctly_drawn(self, plot, savefig):
        self.annotate_and_save_radiograph()
        plot.assert_any_call([2, 4], [2, 4], 'r-', linewidth=0.6)
        plot.assert_any_call([4, 6], [4, 6], 'r-', linewidth=0.6)
        plot.assert_any_call([6, 8], [6, 8], 'r-', linewidth=0.6)
        self.assertEqual(plot.call_count, 3)

    @patch('matplotlib.pyplot.savefig')
    @patch('dysplasia_classification.image_processing.ImageAnnotator.AngleAnnotation')
    def test_annotated_radiograph_draws_arcs_correctly(self, angle_annotation, savefig):
        self.annotate_and_save_radiograph()
        self.assertEqual(angle_annotation.call_count, 2)
        angle_annotation.assert_any_call((4.0, 4.0), (6.0, 6.0), (2.0, 2.0), ax=ANY,size=20, text='0', textposition='inside',
                                         text_kw={'fontsize': 3, 'color': 'blue'})
        angle_annotation.assert_any_call((6.0, 6.0), (8.0, 8.0), (4.0, 4.0), ax=ANY,size=20, text='0', textposition='inside',
                                         text_kw={'fontsize': 3, 'color': 'blue'})

    def annotate_and_save_radiograph(self):
        hip_info = HipInformation((1, 1), (2, 2), (3, 3), (4, 4), 1)
        img = np.zeros((448, 448))
        folder = "folder"
        new_img_name = "img"
        ImageAnnotator.annotate_and_save_radiograph(img, folder, new_img_name, hip_info)
