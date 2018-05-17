from hashlib import sha256
from binascii import hexlify, unhexlify
from unittest import TestCase, main


def doubleSha256(raw_hash_bytes):
    return sha256(sha256(raw_hash_bytes).digest()).digest()


def doubleSha256AndDecode(raw_hash_bytes):
    double_sha256_bytes = doubleSha256(raw_hash_bytes)
    return hexlify(double_sha256_bytes).decode('ascii')


class TestUtilities(TestCase):
    def test_doubleSha256AndDecode(self):
        double_sha256 = doubleSha256AndDecode(unhexlify('e93c0118'))
        assert double_sha256 == '08258cdab9b4c88f91dd393caa4a05e03a49076e6a35fe23ccc0923493d69df0'


if __name__ == '__main__':
    main()
