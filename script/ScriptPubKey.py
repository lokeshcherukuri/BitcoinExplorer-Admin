from unittest import TestCase, main

from core.Address import Address
from script.Script import Script
from .ScriptPattern import ScriptPattern


class ScriptPubKey(Script):
    def __init__(self, script_hex, script_decoded):
        super().__init__(script_hex, script_decoded)

    def __repr__(self):
        return '{{ \n hex: {}, \n asm: {}, \n type: {}, \n reqSigs: {} \n addresses: {} \n }}'.format(
            self.hex, self.asm, self.type, self.reqSigs, self.addresses
        )

    def to_dict(self):
        dictionary = dict(
            hex=self.hex,
            asm=self.asm,
            type=self.type
        )
        if hasattr(self, 'addresses'):
            dictionary['addresses'] = self.addresses
        if hasattr(self, 'reqSigs'):
            dictionary['reqSigs'] = self.reqSigs
        return dictionary

    @classmethod
    def parse(cls, stream):
        script = super().parse(stream)
        script.type = ScriptPattern.findScriptType(script.asm)
        script.addresses = cls.getReceiverAddresses(script.asm, script.type)
        if script.addresses is not None and len(script.addresses) != 0:
            script.reqSigs = len(script.addresses)
        return script

    @staticmethod
    def getReceiverAddresses(script, script_type):
        elements = script.split(' ')
        addresses = []
        if script_type == 'pubkey':
            address = Address.pubKeyToAddress(elements[0])
            if address:
                addresses.append(address)
        elif script_type == 'pubkeyhash':
            address = Address.hash160ToPubKeyHashAddress(elements[2])
            if address:
                addresses.append(address)
        elif script_type == 'scripthash':
            address = Address.hash160ToScriptHashAddress(elements[1])
            if address:
                addresses.append(address)
        elif script_type == 'multisig':
            keys = elements[1:len(elements)-2]
            for key in keys:
                address = Address.pubKeyToAddress(key)
                if address:
                    addresses.append(address)
        return addresses


class TestScriptPubKey(TestCase):
    def test_parse(self):
        print('testing parse')


if __name__ == '__main__':
    main()
