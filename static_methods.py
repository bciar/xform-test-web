"""Static methods"""
import subprocess
import shlex


def _run_background_process(command_line):
    """This method runs external program using command line interface.

    Returns:
         stdout,stdin: Of executed program.
    """

    args = shlex.split(command_line, posix=False)
    process = subprocess.Popen(args, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    process.wait()
    stdout = process.stdout.read().decode().strip()
    stderr = process.stderr.read().decode().strip()

    return stdout, stderr
