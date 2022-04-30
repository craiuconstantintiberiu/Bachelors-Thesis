import os

import cv2

from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from MLPart import load_own_model, predict_image

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

my_model = 2
#my_model = load_own_model("higherResolutionLatest")


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
        # print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        file_dir = "static/uploads/" + filename
        img = cv2.imread(file_dir)

        predict_image(image=img, model=my_model, new_image_name=filename + "_prediction")
        return render_template('upload.html', filename=filename, prediction_filename=filename + "_prediction.jpg")
    else:
        flash('Allowed image types are -> png, jpg, jpeg')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route('/display/<prediction_filename>')
def display_prediction_image(prediction_filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', prediction_filename='predictions/' + prediction_filename), code=301)


if __name__ == "__main__":
    app.run()
