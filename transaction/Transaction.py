import unittest
from io import BytesIO
from binascii import unhexlify
from Utilities import bytes_to_int, varInt
from transaction.TransactionInput import TransactionInput
from transaction.TransactionOutput import TransactionOutput


class Transaction:
    def __init__(self, version, vin, vout):
        self.version = version
        self.vin = vin
        self.vout = vout

    @classmethod
    def parse(cls, stream):
        version = bytes_to_int(stream.read(4))
        vin = cls.parseTxInputs(stream)
        vout = cls.parseTxOutputs(stream)

        return cls(version, vin, vout)

    @staticmethod
    def parseTxInputs(stream):
        vin_size = varInt(stream)
        vin = []
        for i in range(1, vin_size):
            vin.append(TransactionInput.parse(stream))

        return vin

    @staticmethod
    def parseTxOutputs(stream):
        vout_size = varInt(stream)
        vout = []
        for index in range(0, vout_size-1):
            tx_output = TransactionOutput.parse(stream)
            tx_output.n = index
            vout.append(tx_output)

        return vout


class TestTransaction(unittest.TestCase):
    def test_parse(self):
        raw_tx = ""
        tx = Transaction.parse(BytesIO(unhexlify(raw_tx)))
        assert tx
