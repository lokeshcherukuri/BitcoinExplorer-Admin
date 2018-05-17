from binascii import unhexlify, hexlify
from unittest import TestCase, main
from io import BytesIO
from hashlib import sha256
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


def doubleSha256(byte_arr):
    return sha256(sha256(byte_arr).digest()).digest()


def doubleSha256AndDecode(byte_arr):
    double_sha256 = doubleSha256(byte_arr)
    return decodeToAscii(double_sha256)


def decodeToAscii(byte_arr):
    return hexlify(byte_arr).decode('ascii')


def switchEndianAndDecode(byte_arr):
    return decodeToAscii(byte_arr[::-1])


def readAndResetStream(stream, curr_pos, start_pos, end_pos):
    stream.seek(start_pos)
    bytes_arr = stream.read(end_pos-start_pos)
    stream.seek(curr_pos)
    return bytes_arr


def base58Encode(byte_arr):
    return base58.b58encode(byte_arr).decode('ascii')


class TestUtilities(TestCase):
    def test_bytesToInt(self):
        print(bytesToInt(b'01', 'big'))

    def test_var_int(self):
        num = varInt(BytesIO(unhexlify('fd5d01')))
        assert num == 349

    def test_switchEndianAndDecode(self):
        little_endian = 'e93c0118'
        big_endian = switchEndianAndDecode(unhexlify(little_endian))
        assert big_endian == '18013ce9'


if __name__ == '__main__':
    main()
