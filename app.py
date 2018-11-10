"""Web application for XFormTest

http://xform-test.pma2020.org
http://xform-test-docs.pma2020.org
"""
from glob import glob
import platform
import os
import sys

from flask import Flask, render_template, jsonify, request
# noinspection PyProtectedMember
from static_methods import _run_background_process, _run_windows_process
from werkzeug.utils import secure_filename

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
is_windows = platform.system() == 'Windows'
path_char = '\\' if is_windows else '/'
TEMP_DIR = 'temp'
XFORM_TEST_EXECUTABLE = glob('bin/xform-test/*.jar')[0]
LOGGING_ON = os.getenv('FLASK_ENV') in ('development', 'staging') or \
             os.getenv('APP_SETTINGS') in ('development', 'staging')
# Even if there is no error, Heroku always prints this message to the console
# under stderr. I file a bug report. - Joe 2018/11/10
heroku_err_every_time = 'Picked up JAVA_TOOL_OPTIONS: -Xmx300m -Xss512k ' \
                        '-XX:CICompilerCount=2 -Dfile.encoding=UTF-8'


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
            stdout, stderr = _run_background_process(command) if not \
                is_windows else _run_windows_process(command)
            stderr = '' if stderr == heroku_err_every_time else stderr
            if stderr:
                stderr = stderr.replace(heroku_err_every_time, '')
                if LOGGING_ON:
                    print(stderr, file=sys.stderr)
                    print(stdout)
                return render_template('index.html', error=stderr,
                                       stdout=stdout if LOGGING_ON else '')
        else:
            xml = filename

        command = 'java -jar ' + XFORM_TEST_EXECUTABLE + ' ' \
                  + TEMP_DIR + path_char + xml
        stdout, stderr = _run_background_process(command) if not \
            is_windows else _run_windows_process(command)
        stderr = '' if stderr == heroku_err_every_time else stderr
        for file in glob('temp/*'):
            os.remove(file)
        if stderr:
            stderr = stderr.replace(heroku_err_every_time, '')
            if LOGGING_ON:
                print(stderr, file=sys.stderr)
                print(stdout)
            # TODO: @Joe: Fix so CLI does not return this in err msg.
            stderr = stderr.replace(
                'Exception in thread "main" org.pma2020.xform_test.', '')
            return render_template('index.html', error=stderr,
                                   stdout=stdout if LOGGING_ON else '')
        else:
            return render_template('index.html', out=stdout,
                                   error=stderr if LOGGING_ON else '')
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
