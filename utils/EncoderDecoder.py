from binascii import hexlify, unhexlify
from unittest import TestCase, main
import base58


def decodeToAscii(byte_arr):
    return hexlify(byte_arr).decode('ascii')


def switchEndianAndDecode(byte_arr):
    return decodeToAscii(byte_arr[::-1])


def base58Encode(byte_arr):
    return base58.b58encode(byte_arr).decode('ascii')


class TestUtilities(TestCase):
    def test_switchEndianAndDecode(self):
        little_endian = 'e93c0118'
        big_endian = switchEndianAndDecode(unhexlify(little_endian))
        assert big_endian == '18013ce9'


if __name__ == '__main__':
    main()
