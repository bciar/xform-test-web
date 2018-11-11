"""Config"""
from glob import glob
import os
import platform

IS_WINDOWS = platform.system() == 'Windows'
TEMP_DIR = 'temp'
XFORM_TEST_EXECUTABLE = glob('bin/xform-test/*.jar')[0]
LOGGING_ON = os.getenv('FLASK_ENV') in ('development', 'staging') or \
             os.getenv('APP_SETTINGS') in ('development', 'staging')
# Even if there is no error, Heroku always prints this message to the console
# under stderr. I file a bug report. - Joe 2018/11/10
HEROKU_ERR_EVERY_TIME = 'Picked up JAVA_TOOL_OPTIONS: -Xmx300m -Xss512k ' \
                        '-XX:CICompilerCount=2 -Dfile.encoding=UTF-8'
