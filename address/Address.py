from binascii import unhexlify

from utils import EncoderDecoder
from utils import Sha256Hash


class Address:
    def __init__(self, address):
        self.address = address

    def toString(self):
        return self.address

    @classmethod
    def fromHash(cls, network, hashvalue, hashtype):
        prefix = ''
        if hashtype == 'pubkeyhash':
            prefix = b'\x00' if network == 'mainnet' else b'\x6f'
        elif hashtype == 'scripthash':
            prefix = b'\x05' if network == 'mainnet' else b'\xc4'
        hash160_bytes = prefix + unhexlify(hashvalue)
        double_sha256 = Sha256Hash.doubleSha256(hash160_bytes)
        checksum_bytes = double_sha256[:4]
        address = EncoderDecoder.base58Encode(hash160_bytes + checksum_bytes)
        return cls(address)
