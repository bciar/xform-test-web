"""Web application for XFormTest

http://xform-test.pma2020.org
http://xform-test-docs.pma2020.org
"""
import json
from glob import glob
import os
import sys

from flask import Flask, render_template, jsonify, request
from werkzeug.utils import secure_filename

# noinspection PyProtectedMember
from static_methods import _return_failing_result, _run_process
from config import HEROKU_ERR_EVERY_TIME, XFORM_TEST_EXECUTABLE, LOGGING_ON, \
    TEMP_DIR, IS_WINDOWS

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
path_char = '\\' if IS_WINDOWS else '/'


@app.route('/')
def index():
    """Index"""
    return render_template('index.html')


@app.route('/about')
def about():
    """About"""
    return render_template('about.html')


@app.route('/xform_test/<string:filename>')
def xform_test(filename):
    """Runs XFormTest CLI."""
    try:
        if filename.endswith('.xls') or filename.endswith('.xlsx'):
            xml = filename.replace('.xlsx', '.xml').replace('.xls', '.xml')
            command = 'xls2xform ' + TEMP_DIR + path_char + filename + ' ' + \
                      TEMP_DIR + path_char + xml
            stdout, stderr = _run_process(command)
            stderr = '' if stderr == HEROKU_ERR_EVERY_TIME else stderr
            # err when converting to xml
            if stderr:
                return _return_failing_result(stderr, stdout)
        else:
            xml = filename

        command = 'java -jar ' + XFORM_TEST_EXECUTABLE + ' ' \
                  + TEMP_DIR + path_char + xml
        stdout, stderr = _run_process(command)
        stderr = '' if stderr == HEROKU_ERR_EVERY_TIME else stderr
        for file in glob('temp/*'):
            os.remove(file)

        # err when running xform-test
        if stderr:
            return _return_failing_result(stderr, stdout)

        # passing result
        result = json.loads(stdout)
        success = result['successMsg']
        warnings = result['warningsMsg']
        return render_template('index.html', success=success,
                               warnings=warnings,
                               error=stderr if LOGGING_ON else '')
    # unexpected err
    except Exception as err:
        print(str(err), file=sys.stderr)
        return render_template('index.html', error=str(err))


@app.route('/upload', methods=['POST'])
def upload():
    """Upload"""
    try:
        file = request.files['file']
        filename = secure_filename(file.filename)
        upload_folder = basedir + path_char + TEMP_DIR
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


if __name__ == '__main__':
    app.run(debug=True)
