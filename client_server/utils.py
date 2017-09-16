import subprocess
import tempfile
from os import path
import base64
import struct
import time


def b64encode(data):
    if isinstance(data, str):
        return base64.b64encode(data.encode(encoding='UTF-8')).decode()

    return base64.b64encode(data).decode()


def b64decode(data):
    if isinstance(data, str):
        return base64.b64decode(data)

    return base64.b64decode(data.encode(encoding='UTF-8'))


def b64decodestr(data):
    return b64decode(data).decode()


def to_string(data):
    if isinstance(data, str):
        return data
    if isinstance(data, int):
        return str(data)
    else:
        return data.decode()


def create_tmp_file(base_name):
    filename, extension = path.split(base_name)
    return tempfile.TemporaryFile(suffix=extension)


def run_process_split(command, cwd='.'):
    return run_process(command.split(), cwd)


def run_process(command, cwd='.'):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()

    return {
        'ret_code': process.returncode,
        'stdout': to_string(out),
        'stderr': to_string(err)
    }


def read_whole_file(filename, mode='r'):
    with open(filename, mode) as file:
        return file.read()


def read_file_as_b64(filename):
    return b64encode(read_whole_file(filename, 'rb'))


def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)


def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)


def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data


def current_milli_time():
    return int(round(time.time() * 1000))
