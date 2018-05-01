from unittest import TestCase, main

from core.Address import Address
from script.Script import Script
from .ScriptPattern import ScriptPattern


class ScriptPubKey(Script):
    def __init__(self, script_hex, script_decoded, script_type, req_sigs):
        super().__init__(script_hex, script_decoded)
        self.type = script_type
        self.reqSigs = req_sigs

    @staticmethod
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
        # TODO find reqSigs basing on pubkeyscript.
        # if p2pkh, reqSigs is 1
        # if multisig, use m & n values
        # temporarily initializing with 1
        script.reqSigs = 1
        # find addresses
        # hashes = ScriptPattern.getDestinationHashes(script.asm)
        # for hash in hashes:
        #     address = Address.


class TestScriptPubKey(TestCase):
    def test_parse(self):
        print('testing parse')


if __name__ == '__main__':
    main()
