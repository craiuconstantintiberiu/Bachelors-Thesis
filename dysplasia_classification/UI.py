import os

import cv2

from dysplasia_classification.classification.DysplasiaClassifier import DysplasiaClassifier
from dysplasia_classification.image_processing.ImageAnnotator import ImageAnnotator
from dysplasia_classification.prediction.KeypointPredictor import KeypointPredictor
from dysplasia_classification.app import app
from flask import flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

# from MLPart import load_own_model, save_image_and_retrieve_angles

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

my_model = True
# load_own_model("higherResolutionLatest")

predictor = KeypointPredictor()


def get_chosen_models():
    return request.form.getlist('Model')


def generate_file_name_for_prediction(model, image_name):
    return image_name + '_' + model


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
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_dir = "static/uploads/" + filename

        img = cv2.imread(file_dir)

        predictions = predictor.predict_keypoints(img, get_chosen_models())

        display_infos = retrieve_dysplasia_information_and_save_annotated_image(filename, img, predictions)
        return render_template('upload.html', display_infos=display_infos)

    else:
        flash('Allowed image types are -> png, jpg, jpeg')
        return redirect(request.url)


def retrieve_dysplasia_information_and_save_annotated_image(filename, img, predictions):
    display_infos = []
    for model, prediction in zip(get_chosen_models(), predictions):
        left_hip_angle, right_hip_angle = ImageAnnotator.retrieve_angles(prediction)
        new_image_name = generate_file_name_for_prediction(model, filename)
        ImageAnnotator.annotate_and_save_radiograph(img, new_image_name, left_hip_angle, right_hip_angle, prediction)
        left_hip_classification = DysplasiaClassifier.classify_based_on_angle(left_hip_angle).value
        right_hip_classification = DysplasiaClassifier.classify_based_on_angle(right_hip_angle).value

        display_infos.append({"model": model,
                              "left_hip_norberg": left_hip_angle,
                              'left_hip_classification': left_hip_classification,
                              'right_hip_norberg': right_hip_angle,
                              'right_hip_classification': right_hip_classification,
                              'prediction_filename': new_image_name + ".svg"})
    return display_infos


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/display/<prediction_filename>')
def display_prediction_image(prediction_filename):
    return redirect(url_for('static', prediction_filename='predictions/' + prediction_filename), code=301)


if __name__ == "__main__":
    app.run(debug=True)
