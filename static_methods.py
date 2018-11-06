from subprocess import PIPE, run
import shlex
import os


def _run_background_process(command_line):
    """This method runs external program using command line interface.

    Returns:
         stdout,stdin: Of executed program.
    """

    args = shlex.split(command_line, posix=False)
    process = run(args, stdout=PIPE, stderr=PIPE, shell=True, check=True)
    #CompletedProcess()
    # process = subprocess.Popen(['java', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #process.wait()
    stdout = process.stdout
    stderr = process.stderr

    return stdout, stderr

def _run_terminal_command(command_line):
    ret = os.system(command_line)
    return ret

