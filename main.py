import os

import cv2

import dysplasia_classifier
from ImageAnnotator import save_image_and_retrieve_angles
from KeypointPredictor import KeypointPredictor
from app import app
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
# from MLPart import load_own_model, save_image_and_retrieve_angles

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

my_model = True
# load_own_model("higherResolutionLatest")

predictor = KeypointPredictor()


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
        predictions = predictor.predict_keypoints(img,["unet"])
        new_image_name=filename+"_resnetPrediction"
        angle_left, angle_right = save_image_and_retrieve_angles(image=img,
                                                                 new_image_name=new_image_name,
                                                                 prediction=predictions[0])
        left_hip_classification = dysplasia_classifier.classify_based_on_angle(angle_left).name
        right_hip_classification = dysplasia_classifier.classify_based_on_angle(angle_right).name
        return render_template('upload.html', left_hip_norberg=angle_left,
                               left_hip_classification=left_hip_classification,
                               right_hip_norberg=angle_right, right_hip_classification=right_hip_classification
                               , prediction_filename=new_image_name+".svg")
    else:
        flash('Allowed image types are -> png, jpg, jpeg')
        return redirect(request.url)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/display/<prediction_filename>')
def display_prediction_image(prediction_filename):
    return redirect(url_for('static', prediction_filename='predictions/' + prediction_filename), code=301)


if __name__ == "__main__":
    app.run(debug=True)

def getChosenModels():
    request.