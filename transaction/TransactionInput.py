from io import BytesIO
from Utilities import bytesToInt, varInt, decodeToAscii
from script.ScriptSig import ScriptSig
from unittest import TestCase, main


class TransactionInput:
    def __init__(self, txid, vout, script_sig, sequence):
        self.txid = txid
        self.vout = vout
        self.scriptSig = script_sig
        self.sequence = sequence

    def to_dict(self):
        dictionary = dict(
            txid=self.txid,
            vout=self.vout,
            scriptSig=self.scriptSig,
            sequence=self.sequence
        )
        if hasattr(self, 'txinwitness'):
            dictionary['txinwitness'] = self.txinwitness
        return dictionary

    @classmethod
    def parse(cls, stream):
        txid = decodeToAscii(stream.read(32)[::-1])
        vout = bytesToInt(stream.read(4))
        script_len = varInt(stream)
        script_sig = ScriptSig.parse(BytesIO(stream.read(script_len)))
        sequence = bytesToInt(stream.read(4))

        return cls(txid, vout, script_sig, sequence)


class TestTransactionInput(TestCase):
    def test_parse(self):
        print('testing tx input')


if __name__ == '__main__':
    main()
