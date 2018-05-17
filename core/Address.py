import hashlib
from binascii import unhexlify
from hashlib import sha256
from unittest import TestCase, main

from Globals import COMPRESSED_PUBKEY_LENGTH, UNCOMPRESSED_PUBKEY_LENGTH
from Globals import NETWORK
from utils.EncoderDecoder import decodeToAscii, base58Encode
from utils.Sha256Hash import doubleSha256


class Address:
    @staticmethod
    def isPubKey(key):
        if len(key) != COMPRESSED_PUBKEY_LENGTH*2 and len(key) != UNCOMPRESSED_PUBKEY_LENGTH*2:
            return False
        if (not key.startswith('02')) and (not key.startswith('03')) and (not key.startswith('04')):
            return False
        return True

    @staticmethod
    def pubKeyToAddress(pubkey):
        if not Address.isPubKey(pubkey):
            return None
        sha256hash_bytes = sha256(unhexlify(pubkey)).digest()
        ripemd160hash_bytes = hashlib.new('ripemd160', sha256hash_bytes).digest()
        ripemd160hash = decodeToAscii(ripemd160hash_bytes)
        return Address.hash160ToPubKeyHashAddress(ripemd160hash)

    @staticmethod
    def hash160ToPubKeyHashAddress(hash160):
        prefix = ''
        if NETWORK == 'mainnet':
            prefix = b'\x00'
        else:
            prefix = b'\x6f'
        hash160_bytes = prefix + unhexlify(hash160)
        double_sha256 = doubleSha256(hash160_bytes)
        checksum_bytes = double_sha256[:4]
        return base58Encode(hash160_bytes + checksum_bytes)

    @staticmethod
    def hash160ToScriptHashAddress(hash160):
        prefix = ''
        if NETWORK == 'mainnet':
            prefix = b'\x05'
        else:
            prefix = b'\xc4'
        hash160_bytes = prefix + unhexlify(hash160)
        double_sha256 = doubleSha256(hash160_bytes)
        checksum_bytes = double_sha256[:4]
        return base58Encode(hash160_bytes + checksum_bytes)


class TestAddress(TestCase):

    def test_pubKeyToAddress(self):
        pubkey = '041b0e8c2567c12536aa13357b79a073dc4444acb83c4ec7a0e2f99dd7457516c5817242da796924ca4e99947d087fedf9ce467cb9f7c6287078f801df276fdf84'
        address = Address.pubKeyToAddress(pubkey)
        print(address)
        assert address == '1HWqMzw1jfpXb3xyuUZ4uWXY4tqL2cW47J'

    def test_hash160ToPubKeyHashAddress(self):
        hash160 = 'b5bd079c4d57cc7fc28ecf8213a6b791625b8183'
        address = Address.hash160ToPubKeyHashAddress(hash160)
        print(address)
        assert address == '1HZwkjkeaoZfTSaJxDw6aKkxp45agDiEzN'


if __name__ == '__main__':
    main()
