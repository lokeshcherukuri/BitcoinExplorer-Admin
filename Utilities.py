from binascii import unhexlify
from unittest import TestCase, main
from io import BytesIO
from hashlib import sha256


def bytes_to_int(byte_arr, byteorder='little'):
    return int.from_bytes(byte_arr, byteorder=byteorder)


def varInt(stream):
    value = bytes_to_int(stream.read(1), 'big')
    if value < 0xFD:
        return value
    elif value == 0xFD:
        return bytes_to_int(stream.read(2))
    elif value == 0xFE:
        return bytes_to_int(stream.read(4))
    elif value == 0xFF:
        return bytes_to_int(stream.read(8))
    else:
        return RuntimeError("Expecting 0xFD or 0xFE or 0xFF. But " + value + " Found")


def doubleSha256(byte_arr):
    return sha256(sha256(byte_arr).digest()).digest()


class TestUtilities(TestCase):
    def test_bytes_to_int(self):
        print(bytes_to_int(b'01', 'big'))

    def test_var_int(self):
        print(varInt(BytesIO(unhexlify('fd0302'))))


if __name__ == '__main__':
    main()
