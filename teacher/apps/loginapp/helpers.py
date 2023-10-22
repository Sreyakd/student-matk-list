
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
from cryptography.hazmat.backends import default_backend
from base64 import  b64decode, b64encode
from cryptography.hazmat.primitives.padding import PKCS7



class DataEncryption():


    def encrypt(key, plaintext):
        iv                  = os.urandom(16)
        cipher              = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor           = cipher.encryptor()
        padder              = PKCS7(128).padder()
        padded_plaintext    = padder.update(plaintext.encode("utf-8")) + padder.finalize()
        ciphertext          = encryptor.update(padded_plaintext) + encryptor.finalize()
        return b64encode(iv + ciphertext).decode("utf-8")


    def decrypt(key, ciphertext):
        ciphertext = b64decode(ciphertext.encode("utf-8"))
        iv = ciphertext[:16]
        ciphertext = ciphertext[16:]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder = PKCS7(128).unpadder()
        decrypted_plaintext_padded = unpadder.update(decrypted_padded) + unpadder.finalize()

        plaintext = decrypted_plaintext_padded.decode("utf-8")
        return plaintext