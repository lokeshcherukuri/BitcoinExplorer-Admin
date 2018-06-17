from Utilities import bytesToInt, varInt
from utils.EncoderDecoder import decodeToAscii, switchEndianAndDecode
from io import BytesIO
from core.script.ScriptSig import ScriptSig
from unittest import TestCase, main


class TransactionInput:
    def __init__(self, coinbase, sequence, prev_txid, prev_output_index=None, script_signature=None):
        if coinbase is not None:
            self.coinbase = coinbase
        else:
            self.prev_txid = prev_txid
            self.prev_output_index = prev_output_index
            self.script_signature = script_signature
        self.sequence = sequence

    def __repr__(self):
        if hasattr(self, 'coinbase'):
            return "{{ \n coinbase: {}, \n sequence: {} \n }}".format(
                self.coinbase, self.sequence
            )
        else:
            return "{{ \n prev_txid: {},\n prev_output_index: {}, \n script_signature: {}, \n sequence: {} \n }}".format(
                self.prev_txid, self.prev_output_index, self.script_signature, self.sequence
            )

    def toString(self):
        if hasattr(self, 'coinbase'):
            return dict(
                coinbase=self.coinbase,
                sequence=self.sequence
            )
        else:
            dictionary = dict(
                prev_txid=self.prev_txid,
                prev_output_index=self.prev_output_index,
                script_signature=self.script_signature,
                sequence=self.sequence
            )
            if hasattr(self, 'txinwitness'):
                dictionary['txinwitness'] = self.txinwitness
            return dictionary

    @classmethod
    def parse(cls, stream):
        prev_txid = switchEndianAndDecode(stream.read(32))
        prev_output_index = bytesToInt(stream.read(4))
        script_length = varInt(stream)

        if int(prev_txid, 16) == 0:
            coinbase = decodeToAscii(stream.read(script_length))
            sequence = bytesToInt(stream.read(4))
            return cls(coinbase, sequence, None, None, None)
        else:
            script_signature = ScriptSig.parse(BytesIO(stream.read(script_length)))
            sequence = bytesToInt(stream.read(4))
            return cls(None, sequence, prev_txid, prev_output_index, script_signature)


class TestTransactionInput(TestCase):
    def test_parse(self):
        print('testing tx input')


if __name__ == '__main__':
    main()
