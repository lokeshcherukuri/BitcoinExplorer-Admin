import base58
import Globals
from Utilities import doubleSha256
from binascii import hexlify, unhexlify
from unittest import TestCase, main


class Address:
    @staticmethod
    def hash160ToPubKeyHashAddress(hash160):
        prefix = ''
        if Globals.NETWORK == 'mainnet':
            prefix = b'\x00'
        else:
            prefix = b'\x6f'
        hash160_bytes = prefix + unhexlify(hash160)
        double_sha256 = doubleSha256(hash160_bytes)
        checksum_bytes = double_sha256[:4]
        return base58.b58encode(hash160_bytes + checksum_bytes)

    @staticmethod
    def hash160ToScriptHashAddress(hash160):
        prefix = ''
        if Globals.NETWORK == 'mainnet':
            prefix = b'\x05'
        else:
            prefix = b'\xc4'
        hash160_bytes = prefix + unhexlify(hash160)
        double_sha256 = doubleSha256(hash160_bytes)
        checksum_bytes = double_sha256[:4]
        return base58.b58encode(hexlify(hash160_bytes + checksum_bytes))


class TestAddress(TestCase):
    def test_hash160ToPubKeyHashAddress(self):
        hash160 = 'b5bd079c4d57cc7fc28ecf8213a6b791625b8183'
        address = Address.hash160ToPubKeyHashAddress(hash160)
        print(address)


if __name__ == '__main__':
    main()
