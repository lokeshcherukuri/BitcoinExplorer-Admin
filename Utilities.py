from binascii import unhexlify, hexlify
from unittest import TestCase, main
from io import BytesIO
from hashlib import sha256


def bytesToInt(byte_arr, byteorder='little'):
    return int.from_bytes(byte_arr, byteorder=byteorder)


def varInt(stream):
    value = bytesToInt(stream.read(1), 'big')
    if value < 0xFD:
        return value
    elif value == 0xFD:
        return bytesToInt(stream.read(2))
    elif value == 0xFE:
        return bytesToInt(stream.read(4))
    elif value == 0xFF:
        return bytesToInt(stream.read(8))
    else:
        return RuntimeError("Expecting 0xFD or 0xFE or 0xFF. But " + value + " Found")


def doubleSha256(byte_arr):
    return sha256(sha256(byte_arr).digest()).digest()


def doubleSha256AndDecode(byte_arr):
    double_sha256 = doubleSha256(byte_arr)
    return decodeToAscii(double_sha256)


def decodeToAscii(byte_arr):
    return hexlify(byte_arr).decode('ascii')


class TestUtilities(TestCase):
    def test_bytes_to_int(self):
        print(bytesToInt(b'01', 'big'))

    def test_var_int(self):
        print(varInt(BytesIO(unhexlify('fd0302'))))


if __name__ == '__main__':
    main()
