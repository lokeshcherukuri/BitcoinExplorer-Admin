from io import BytesIO
from unittest import TestCase, main
from Utilities import bytes_to_int, varInt
from script.ScriptPubKey import ScriptPubKey


class TransactionOutput:
    def __init__(self, value, script_pubkey):
        self.value = value
        self.scriptPubKey = script_pubkey

    def to_dict(self):
        return dict(
            value=self.value,
            scriptPubKey=self.scriptPubKey
        )

    @classmethod
    def parse(cls, stream):
        value = bytes_to_int(stream.read(8))
        script_pubkey_len = varInt(stream)
        script_pubkey = ScriptPubKey.parse(BytesIO(stream.read(script_pubkey_len)))

        return cls(value, script_pubkey)


class TestTransactionOutput(TestCase):
    def test_parse(self):
        print('testing tx output')


if __name__ == '__main__':
    main()
