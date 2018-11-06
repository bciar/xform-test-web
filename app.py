import os
from flask import Flask, render_template, jsonify, request, redirect
from static_methods import _run_background_process, _run_terminal_command
from werkzeug.utils import secure_filename
from flask import flash

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/xform_test/<string:filename>')
def xform_test(filename):
    '''ret = _run_terminal_command('java -jar xform-test-0.3.0.jar temp_uploads\\MultipleTestCases.xml')
    print('return value', ret)'''
    try:
        stdout, stderr = _run_background_process('java -jar xform-test-0.3.0.jar temp_uploads\\'+filename)
        error = stderr.decode("utf-8")
        out = stdout.decode("utf-8")
        # flash(out, "warning")
        return render_template('index.html', **locals())
    except Exception as err:
        error = err.stderr.decode("utf-8")
        return render_template('index.html', **locals())

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

        return jsonify({'success': True, 'filename': filename})
    except Exception as err:
        msg = 'An unexpected error occurred:\n\n' + str(err)
        return jsonify({'success': False, 'message': msg})

if __name__=='__main__':
    app.run(debug=True)