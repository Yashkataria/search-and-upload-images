
from flask import Flask, render_template, url_for, redirect, send_from_directory, request, flash, session, jsonify
import os, logging
from werkzeug.utils import secure_filename
import numpy as np
from CNN_classifier import FeatureExtractor
from PIL import Image
from pathlib import Path

app = Flask(__name__)

HOME_FOLDER = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/img'.format(HOME_FOLDER)
ALLOWED_EXTENSIONS = set(['jpg','png','jpeg','gif'])

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler('server.log')
handler.setLevel(level=logging.INFO)

log_formatter = logging.Formatter("%(asctime)s - %(message)s")
handler.setFormatter(log_formatter)

logger.addHandler(handler)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024
app.secret_key = 'h233'

CNN = FeatureExtractor()
features = []
img_names = []
for feature_path in os.listdir( app.config['UPLOAD_FOLDER']+'/../feature'):
    features.append(np.load(app.config['UPLOAD_FOLDER']+'/../feature/'+feature_path))
    img_names.append(Path("./upload/") / (feature_path.split('.')[0] + ".jpg"))
features = np.array(features)

def check_file_extension(filename):
    logging.info('Checking file extension')
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        return True
    return False

def create_new_folder(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return  dir_path 

def get_file(path):
    """Download a file."""
    return send_from_directory(UPLOAD_FOLDER, path, as_attachment=True)

@app.route('/')
def home():
    return render_template('home.html', names=os.listdir(app.config['UPLOAD_FOLDER']))

@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        logging.info(app.config['UPLOAD_FOLDER'])
        if 'files[]' not in request.files:
            flash('No file')
            return redirect(url_for('home'))
        images = request.files.getlist('files[]')
        for _file in images:
            if _file.filename == '':
                flash('No selected file')
                return redirect(url_for('home'))
            if _file and check_file_extension(_file.filename):
                logging.info('Saving file')
                filename = secure_filename(_file.filename)
                create_new_folder(app.config['UPLOAD_FOLDER'])
                saved_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                _file.save(saved_path)
                session[filename] = True
            else:
                flash('Only images are allowed')
                return redirect(url_for('home'))
        logging.info('File saved')
        flash('File(s) saved')
        return redirect(url_for('home'))        
    return redirect(url_for('home'))

@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        logging.info(app.config['UPLOAD_FOLDER'])
        image = request.files['query_img']
        if image.filename == '':
            flash('No selected file')
            return redirect(url_for('home'))
        if image and check_file_extension(image.filename):

            img = Image.open(image.stream)

            query = CNN.extract(img)
            dists = np.linalg.norm(features-query, axis=1)  # L2 distances to features
            ids = np.argsort(dists)[:10]  # Top 10 results
            scores = [(dists[id], img_names[id]) for id in ids]
            logging.info(scores)
            logging.info('Saving file')
            filename = secure_filename(image.filename)
            create_new_folder(app.config['UPLOAD_FOLDER'])
            saved_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(saved_path)
            session[filename] = True
        else:
            flash('Only images are allowed')
            return redirect(url_for('home'))
        logging.info('File saved')
        flash('File(s) saved')
        return render_template('home.html', image_name=image.filename,
                               scores=scores)   
    return redirect(url_for('home'))

if __name__ == "__main__": 
    app.run(host ='0.0.0.0', port = 5001)
