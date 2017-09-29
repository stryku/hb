from aes import *
import utils


class EncryptedFile:
    def __init__(self, filename=None):
        key = utils.read_whole_file('aes.password')
        self.cipher = AESCipher(key)
        if filename:
            self.open(filename)
        else:
            self.file = None

    def open(self, filename):
        self.file = open(filename, 'r+b')

    def close(self):
        self.file.close()

    def write(self, data):
        encrypted = self.cipher.encrypt(data)
        self.file.write(encrypted)

    def read(self):
        encrypted = self.file.read()
        return self.cipher.decrypt(encrypted)

