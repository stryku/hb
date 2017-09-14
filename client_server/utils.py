import subprocess
import tempfile
from os import path


def create_tmp_file(base_name):
    filename, extension = path.split(base_name)
    return tempfile.TemporaryFile(suffix=extension)


def run_process(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()

    return {
        'ret_code': process.returncode,
        'stdout': out,
        'stderr': err
    }
