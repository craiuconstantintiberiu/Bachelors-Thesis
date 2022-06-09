import os

import cv2

from dysplasia_classification.prediction.HipProcessor import HipProcessor
from dysplasia_classification.image_processing.ImageAnnotator import ImageAnnotator
from dysplasia_classification.image_processing.ImageUtils import ImageUtils
from dysplasia_classification.prediction.KeypointPredictor import KeypointPredictor
from dysplasia_classification.app import app
from flask import flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

processor = HipProcessor(None)


def get_chosen_models():
    return request.form.getlist('Model')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        return return_hip_information_and_annotated_radiographs(file)
    else:
        flash('Allowed image types are -> png, jpg, jpeg')
        return redirect(request.url)


def return_hip_information_and_annotated_radiographs(file):
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    img = cv2.imread(file_path)
    hip_infos = processor.process_radiograph(img, get_chosen_models(), filename)
    return render_template('upload.html', hip_infos=hip_infos)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/display/<file_name>')
def display_prediction_image(file_name):
    return redirect(url_for('static', file_name='predictions/' + file_name), code=301)


if __name__ == "__main__":
    predictor = KeypointPredictor()
    processor.keypoint_predictor = predictor
    app.run(debug=True, host='0.0.0.0')
