import os.path

from flask import Flask

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__),'static/uploads/')
PREDICTIONS_FOLDER=os.path.join(os.path.dirname(__file__),'static/predictions/')

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PREDICTIONS_FOLDER'] = PREDICTIONS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024