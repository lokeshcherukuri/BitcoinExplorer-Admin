from binascii import hexlify
from Utilities import bytes_to_int
from Utilities import varInt
from script.ScriptSig import ScriptSig
from unittest import TestCase, main


class TransactionInput:
    def __init__(self, txid, vout, script_sig, sequence):
        self.txid = txid
        self.vout = vout
        self.script_sig = script_sig
        self.sequence = sequence

    @classmethod
    def parse(cls, stream):
        txid = hexlify(stream.read(32)).decode('ascii')
        vout = bytes_to_int(stream.read(4))
        script_len = varInt(stream)
        script_sig = ScriptSig.parse(stream.read(script_len))
        sequence = bytes_to_int(stream.read(4))

        return cls(txid, vout, script_sig, sequence)


class TestTransactionInput(TestCase):
    def test_parse(self):
        print('testing tx input')


if __name__ == '__main__':
    main()
