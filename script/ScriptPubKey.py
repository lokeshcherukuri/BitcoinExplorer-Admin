from unittest import TestCase, main

from core.Address import Address
from script.Script import Script
from .ScriptPattern import ScriptPattern


class ScriptPubKey(Script):
    def __init__(self, script_hex, script_decoded, script_type=None, req_sigs=None):
        super().__init__(script_hex, script_decoded)
        self.type = script_type
        self.reqSigs = req_sigs

    def to_dict(self):
        return dict(
            hex=self.hex,
            asm=self.asm,
            type=self.type,
            reqSigs=self.reqSigs
        )

    @classmethod
    def parse(cls, stream):
        script = super().parse(stream)
        script_type = ScriptPattern.findScriptType(script.asm)
        script.type = script_type
        script.reqSigs = 1
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
    def getDestinationAddresses(script):
        # find addresses
        # hashes = ScriptPattern.getDestinationHashes(script.asm)
        # for hash in hashes:
        #     find address
        pass


class TestScriptPubKey(TestCase):
    def test_parse(self):
        print('testing parse')


if __name__ == '__main__':
    main()
