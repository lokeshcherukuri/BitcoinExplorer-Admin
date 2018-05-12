from unittest import TestCase, main

from core.Address import Address
from script.Script import Script
from .ScriptPattern import ScriptPattern


class ScriptPubKey(Script):
    def __init__(self, script_hex, script_decoded, script_type=None, req_sigs=None):
        super().__init__(script_hex, script_decoded)
        self.type = script_type
        self.reqSigs = req_sigs

    def __repr__(self):
        return '{{ \n hex: {}, \n asm: {}, \n type: {}, \n reqSigs: {} \n addresses: {} \n }}'.format(
            self.hex, self.asm, self.type, self.reqSigs, self.addresses
        )

    def to_dict(self):
        return dict(
            hex=self.hex,
            asm=self.asm,
            type=self.type,
            reqSigs=self.reqSigs,
            addresses=self.addresses
        )

    @classmethod
    def parse(cls, stream):
        script = super().parse(stream)
        script_type = ScriptPattern.findScriptType(script.asm)
        script.type = script_type
        script.reqSigs = 1
        script.addresses = cls.getDestinationAddresses(script.asm, script.type)
        return script

    @staticmethod
    def numberOfSigsReqToSpend(script, script_type):
        if script_type == 'pay-to-pubkey-hash':
            script.reqSigs = 1
            pass
        elif script_type == 'pay-to-script-hash':
            pass
        else:
            RuntimeError("Not implemented")

    @staticmethod
    def getDestinationAddresses(script, script_type):
        elements = script.split(' ')
        addresses = []
        if script_type == 'pay-to-pubkey':
            address = Address.pubKeyToAddress(elements[0])
            if address:
                addresses.append(address)
        elif script_type == 'pay-to-pubkey-hash':
            address = Address.hash160ToPubKeyHashAddress(elements[2])
            if address:
                addresses.append(address)
        elif script_type == 'pay-to-script-hash':
            address = Address.hash160ToScriptHashAddress(elements[1])
            if address:
                addresses.append(address)
        elif script_type == 'multisig':
            keys = elements[1:len(elements)-2]
            for key in keys:
                address = Address.pubKeyToAddress(key)
                if address:
                    addresses.append(address)
        else:
            pass

        return addresses


class TestScriptPubKey(TestCase):
    def test_parse(self):
        print('testing parse')


if __name__ == '__main__':
    main()
