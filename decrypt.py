#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Encryption Library AES-256
"""
from Crypto.Cipher import AES

class Decrypt:
    """ Decryption methods """

    _shift = b'\xdd\x84\xa1\x9e\x7f3\xaf\xc5\x87B)p\xa7\x7f\xa2\xba\xe9\xb6lp\xf2\xf5\xa8\xd17\xa8Q\xe4\xd8\xc7\x820'  # pylint: disable=C0301

    def decrypt(self, ciphertext, key=None) -> str:
        """decrypt message

            :param ciphertext: text you want to decrypt
            :param key: bit key

           Returns: Un-padded string
        """
        iv_pad = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv_pad)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, file_name):
        """ decrypt a file (UTF-8)

            :param file_name: file to decrypt
        """
        with open(file_name, 'rb') as document:
            ciphertext = document.read()

        dec = self.decrypt(ciphertext=ciphertext, key=self._shift)
        return dec.decode("utf-8")


