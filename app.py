import os
from flask import Flask, render_template, jsonify, request, redirect, send_file
from data import data
from werkzeug.utils import secure_filename

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/data')
def data():
    DT = data()
    return render_template('data.html', data = DT)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        filename = secure_filename(file.filename)
        upload_folder = basedir + '\\temp_uploads'
        file_path = os.path.join(upload_folder, filename)

        try:
            file.save(file_path)
        except FileNotFoundError:
            os.mkdir(upload_folder)
            file.save(file_path)

        # remove temp file
        # if os.path.exists(file_path):
        #    os.remove(file_path)

        return jsonify({'success': True})
    except Exception as err:
        msg = 'An unexpected error occurred:\n\n' + str(err)
        return jsonify({'success': False, 'message': msg})

if __name__=='__main__':
    app.run(debug=True)