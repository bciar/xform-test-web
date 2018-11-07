from subprocess import PIPE, run, Popen
import shlex
import os


def _run_background_process(command_line):
    """This method runs external program using command line interface.

    Returns:
         stdout,stdin: Of executed program.
    """

    args = shlex.split(command_line, posix=False)
    '''process = run(args, stdout=PIPE, stderr=PIPE, shell=True, check=True)
    stdout = process.stdout
    stderr = process.stderr'''

    process = Popen(args, stdout=PIPE, stderr=PIPE)
    process.wait()
    stdout = process.stdout.read().decode().strip()
    stderr = process.stderr.read().decode().strip()

    return stdout, stderr

def _run_windows_process(command_line):
    args = shlex.split(command_line, posix=False)
    process = run(args, stdout=PIPE, stderr=PIPE, shell=True, check=True)
    stdout = process.stdout.decode("utf-8")
    stderr = process.stderr.decode("utf-8")

    return stdout, stderr

