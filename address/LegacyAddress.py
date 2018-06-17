import hashlib
from binascii import unhexlify
from unittest import TestCase, main

from utils.EncoderDecoder import decodeToAscii
from .Address import Address


class LegacyAddress(Address):
    COMPRESSED_PUBKEY_LENGTH = 33
    UNCOMPRESSED_PUBKEY_LENGTH = 65

    def __init__(self, address):
        super().__init__(address)

    @staticmethod
    def isPubKey(key):
        if len(key) != LegacyAddress.COMPRESSED_PUBKEY_LENGTH * 2 and \
                len(key) != LegacyAddress.UNCOMPRESSED_PUBKEY_LENGTH * 2:
            return False
        if (not key.startswith('02')) and (not key.startswith('03')) and (not key.startswith('04')):
            return False
        return True

    @classmethod
    def fromPubKey(cls, pubkey):
        if not LegacyAddress.isPubKey(pubkey):
            return None
        sha256hash_bytes = hashlib.sha256(unhexlify(pubkey)).digest()
        ripemd160hash_bytes = hashlib.new('ripemd160', sha256hash_bytes).digest()
        ripemd160hash = decodeToAscii(ripemd160hash_bytes)
        return LegacyAddress.fromPubKeyHash(ripemd160hash)

    @classmethod
    def fromPubKeyHash(cls, pubkeyhash):
        return super().fromHash("mainnet", pubkeyhash, "pubkeyhash")

    @classmethod
    def fromScriptHash(cls, scripthash):
        return super().fromHash("mainnet", scripthash, "scripthash")


class TestLegacyAddress(TestCase):

    def test_fromPubKey(self):
        pubkey = '041b0e8c2567c12536aa13357b79a073dc4444acb83c4ec7a0e2f99dd7457516c5817242da796924ca4e99947d087fedf9ce467cb9f7c6287078f801df276fdf84'
        address = LegacyAddress.fromPubKey(pubkey)
        assert address.address == '1HWqMzw1jfpXb3xyuUZ4uWXY4tqL2cW47J'

    def test_fromPubKeyHash(self):
        pubkeyhash = 'b5bd079c4d57cc7fc28ecf8213a6b791625b8183'
        address = LegacyAddress.fromPubKeyHash(pubkeyhash)
        assert address.address == '1HZwkjkeaoZfTSaJxDw6aKkxp45agDiEzN'


if __name__ == '__main__':
    main()