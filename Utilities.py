from binascii import unhexlify
from io import BytesIO
from unittest import TestCase, main

import base58


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


def readAndResetStream(stream, curr_pos, start_pos, end_pos):
    stream.seek(start_pos)
    bytes_arr = stream.read(end_pos-start_pos)
    stream.seek(curr_pos)
    return bytes_arr


class TestUtilities(TestCase):
    def test_bytesToInt(self):
        print(bytesToInt(b'01', 'big'))

    def test_var_int(self):
        num = varInt(BytesIO(unhexlify('fd5d01')))
        assert num == 349


if __name__ == '__main__':
    main()
