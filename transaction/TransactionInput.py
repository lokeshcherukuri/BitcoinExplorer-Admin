from Utilities import bytesToInt, varInt
from utils.EncoderDecoder import decodeToAscii, switchEndianAndDecode
from io import BytesIO
from script.ScriptSig import ScriptSig
from unittest import TestCase, main


class TransactionInput:
    def __init__(self, coinbase, sequence, txid, vout=None, script_sig=None):
        if coinbase is not None:
            self.coinbase = coinbase
        else:
            self.txid = txid
            self.vout = vout
            self.scriptSig = script_sig
        self.sequence = sequence

    def __repr__(self):
        if hasattr(self, 'coinbase'):
            return "{{ \n coinbase: {}, \n sequence: {} \n }}".format(
                self.coinbase, self.sequence
            )
        else:
            return "{{ \n txid: {},\n vout: {}, \n scriptSig: {}, \n sequence: {} \n }}".format(
                self.txid, self.vout, self.scriptSig, self.sequence
            )

    def toString(self):
        if hasattr(self, 'coinbase'):
            return dict(
                coinbase=self.coinbase,
                sequence=self.sequence
            )
        else:
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
        txid = switchEndianAndDecode(stream.read(32))
        vout = bytesToInt(stream.read(4))
        script_length = varInt(stream)

        if int(txid, 16) == 0:
            coinbase = decodeToAscii(stream.read(script_length))
            sequence = bytesToInt(stream.read(4))
            return cls(coinbase, sequence, None, None, None)
        else:
            script_sig = ScriptSig.parse(BytesIO(stream.read(script_length)))
            sequence = bytesToInt(stream.read(4))
            return cls(None, sequence, txid, vout, script_sig)


class TestTransactionInput(TestCase):
    def test_parse(self):
        print('testing tx input')


if __name__ == '__main__':
    main()
