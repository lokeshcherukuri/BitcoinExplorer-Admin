from io import BytesIO
from unittest import TestCase, main
from Utilities import bytesToInt, varInt
from core.script.ScriptPubKey import ScriptPubKey


class TransactionOutput:
    def __init__(self, output_value, script_pubkey):
        self.output_value = output_value
        self.scriptPubKey = script_pubkey

    def __repr__(self):
        return "{{ \n output_value: {}\n scriptPubKey: {}\n }}".format(
            self.output_value, self.scriptPubKey
        )

    def toString(self):
        return dict(
            output_value=self.output_value,
            output_index=self.output_index,
            scriptPubKey=self.scriptPubKey
        )

    @classmethod
    def parse(cls, stream):
        output_value = bytesToInt(stream.read(8))
        script_pubkey_len = varInt(stream)
        script_pubkey = ScriptPubKey.parse(BytesIO(stream.read(script_pubkey_len)))
        return cls(output_value, script_pubkey)


class TestTransactionOutput(TestCase):
    def test_parse(self):
        print('testing tx output')


if __name__ == '__main__':
    main()
