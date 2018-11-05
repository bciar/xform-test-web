import os
from flask import Flask, render_template, jsonify, request, redirect, send_file
from static_methods import _run_background_process
from werkzeug.utils import secure_filename

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/test')
def test():
    stdout, stderr = _run_background_process('java -jar xform-test-0.3.0.jar temp_uploads\\MultipleTestCases.xml')
    print('stdout', stdout, '\n')
    print('stderr', stderr, '\n')
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        filename = secure_filename(file.filename)
        upload_folder = basedir + '\\temp_uploads'
        file_path = os.path.join(upload_folder, filename)

        if os.path.exists(file_path):
           os.remove(file_path)

        try:
            file.save(file_path)
        except FileNotFoundError:
            os.mkdir(upload_folder)
            file.save(file_path)

        return jsonify({'success': True})
    except Exception as err:
        msg = 'An unexpected error occurred:\n\n' + str(err)
        return jsonify({'success': False, 'message': msg})

if __name__=='__main__':
    app.run(debug=True)