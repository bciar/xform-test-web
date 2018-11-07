"""Static utilities for running subprocesses."""
from subprocess import PIPE, run, Popen
import shlex


def _run_background_process(command_line):
    """Run external program using command line interface.

    Returns:
         stdout,stdin: Of executed program.
    """
    args = shlex.split(command_line, posix=False)
    process = Popen(args, stdout=PIPE, stderr=PIPE)
    process.wait()
    stdout = process.stdout.read().decode().strip()
    stderr = process.stderr.read().decode().strip()

    return stdout, stderr


def _run_windows_process(command_line):
    """Run external program using command line interface on Windows.

    Returns:
         stdout,stdin: Of executed program.
    """
    args = shlex.split(command_line, posix=False)
    process = run(args, stdout=PIPE, stderr=PIPE, shell=True, check=True)
    stdout = process.stdout.decode("utf-8")
    stderr = process.stderr.decode("utf-8")

    return stdout, stderr
