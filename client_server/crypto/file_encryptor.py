import os
from crypto.aes import AESCipher
import utils


class EncryptedFile:
    def __init__(self, filename=None, sufix = '.encrypted'):
        key = utils.read_whole_file('aes.password', 'r')
        self.cipher = AESCipher(key)
        self.base_filename = filename
        self.sufix = sufix
        if filename:
            self.open(filename)
        else:
            self.file = None

    def open(self, filename):
        encrypted_name = filename + self.sufix
        self.base_filename = filename
        if os.path.isfile(encrypted_name):
            self.file = open(encrypted_name, 'r+b')
        else:
            self.file = open(encrypted_name, 'a+b')

    def close(self):
        self.file.close()

    def write(self, data):
        encrypted = self.cipher.encrypt(data)
        self.file.write(utils.to_bytes(encrypted))

    def read(self):
        encrypted = self.file.read()
        return self.cipher.decrypt(encrypted)

    def decrypt_to_file(self):
        with open(self.base_filename, 'wb') as file:
            file.write(self.read())

    def encrypt_file(self, filename):
        self.close()
        data = utils.read_whole_file(filename, 'rb')
        self.open(filename)
        self.write(data)

