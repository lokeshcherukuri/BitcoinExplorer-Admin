import unittest
from io import BytesIO
from binascii import unhexlify, hexlify
from ComplexEncoder import ComplexEncoder
from Utilities import bytes_to_int, varInt
from transaction.TransactionInput import TransactionInput
from transaction.TransactionOutput import TransactionOutput
import json


class Transaction:
    def __init__(self, version, vin, vout):
        self.version = version
        self.vin = vin
        self.vout = vout

    def to_dict(self):
        return dict(
            version=self.version,
            vin=self.vin,
            vout=self.vout
        )

    @classmethod
    def parse(cls, stream):
        version = bytes_to_int(stream.read(4))
        is_tx_segwit = cls.isTxSegwit(stream)
        vin = cls.parseTxInputs(stream)
        vout = cls.parseTxOutputs(stream)
        if is_tx_segwit:
            for tx_input in vin:
                txin_witness = cls.parseWitness(stream)
                tx_input.txinwitness = txin_witness
        return cls(version, vin, vout)

    @staticmethod
    def isTxSegwit(stream):
        reset_stream_pos = stream.tell()
        marker = bytes_to_int(stream.read(1))
        if marker != 0x00:
            stream.seek(reset_stream_pos)
            return False
        flag = bytes_to_int(stream.read(1))
        if flag != 0x01:
            stream.seek(reset_stream_pos)
            return False
        return True

    @staticmethod
    def parseTxInputs(stream):
        vin_size = varInt(stream)
        vin = []
        for index in range(0, vin_size):
            vin.append(TransactionInput.parse(stream))
        return vin

    @staticmethod
    def parseTxOutputs(stream):
        vout_size = varInt(stream)
        vout = []
        for index in range(0, vout_size):
            tx_output = TransactionOutput.parse(stream)
            tx_output.n = index
            vout.append(tx_output)
        return vout

    @staticmethod
    def parseWitness(stream):
        witness_stack_size = varInt(stream)
        witness_stack = []
        for index in range(0, witness_stack_size):
            witness_stack_item_length = varInt(stream)
            witness = hexlify(stream.read(witness_stack_item_length)).decode('ascii')
            witness_stack.append(witness)
        return witness_stack


class TestTransaction(unittest.TestCase):
    def test_parse(self):
        # coinbase tx
        # raw_transaction = '01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff5e03d71b07254d696e656420627920416e74506f6f6c20626a31312f4542312f4144362f43205914293101fabe6d6d678e2c8c34afc36896e7d9402824ed38e856676ee94bfdb0c6c4bcd8b2e5666a0400000000000000c7270000a5e00e00ffffffff01faf20b58000000001976a914338c84849423992471bffb1a54a8d9b1d69dc28a88ac00000000'
        # transaction = Transaction.parse(BytesIO(unhexlify(raw_transaction)))
        # assert transaction.txid == '51bdce0f8a1edd5bc023fd4de42edb63478ca67fc8a37a6e533229c17d794d3f'
        # print(json.dumps(transaction.to_dict(), cls=ComplexEncoder, indent=2))

        # pubkeyhash and scripthash outputs
        raw_transaction = '01000000017cc121bf0baf0a38b36697bb4d6a24edb13efb2ca7de277e8a7f7b015121f75c010000006a473044022071d4bb63c23ebcb70fe38d51731564199541ab3ad74ce2667488a932cb673333022059a235d87caaeb7b5786036a6d6debdcda5b20bb2f96dd7b43f039f2640f3c9401210375522818c3b28945fc4bde4a9429dcd8a4ef01fd7f7c2a1407306abc22e4c5d5feffffff025023bf1f000000001976a914e33a59763b5e008f8e20cb23c765fe7ed000b66188ac924344000000000017a914b549a78d07c2fa029eaa1b2b6effac8064e6a36f872fc80700'
        transaction = Transaction.parse(BytesIO(unhexlify(raw_transaction)))
        # assert transaction.txid == '4e66a9188eca7e43c2d169d87f5b2319dc2c19726b8ba0af38adb88492f6a406'
        print(json.dumps(transaction.to_dict(), cls=ComplexEncoder, indent=2))

        # segwit tx with witness
        raw_transaction = '01000000000102d9028184f9dc166b4c59bafcaaf2a2a21440c832c7994e74a7871eb25aac386501000000171600144d9458205311924ff38df9096e55a68494613eb5ffffffffdb31fe7f8a9df2c7fd65720bd67a1977d94638464f7fa999309eb1976dd7e0fa01000000171600141f7765aed84e6afc0d67a699c126e7c4d38e2121ffffffff0280778e06000000001976a9141d0efca73a712e0116dfe77a20926aeb9378460488acdd28da590700000017a9144daba1dc5807d203253cf10ee55a751f85403a79870247304402200dae39e241bc21c389ae9da74d77bb12a4b26b704c198a994195c99324089fb80220363bae82fa825f25882353c81b1bf2715b62fe38cc6de0366e5ef0125ccbd1af01210256f76143ff6b467ee50bf3f35a83290b7ccbc17af055bfb1d53e465afb921bab02483045022100a3b0c314e67d7d22355181b36ab857a75652abbd74007909557048cf137ec98c0220574b7f895573c35b2f9bea6582b7ae5cf70f2d330ae83fe41cdf6b74e417af01012103d8271f9886f2c4be689f7bbf0f8b38a24b9ebd309d9f88cd4da4c2adc22c6dce00000000'
        transaction = Transaction.parse(BytesIO(unhexlify(raw_transaction)))
        # assert transaction.txid == '058fc390bb3a966bc59a627af80a3139b407e50a6b24ce9b659841b87bd0f6a1'
        print(json.dumps(transaction.to_dict(), cls=ComplexEncoder, indent=2))
        #
        raw_transaction = '01000000013dcd7d87904c9cb7f4b79f36b5a03f96e2e729284c09856238d5353e1182b00200000000fd5d01004730440220762ce7bca626942975bfd5b130ed3470b9f538eb2ac120c2043b445709369628022051d73c80328b543f744aa64b7e9ebefa7ade3e5c716eab4a09b408d2c307ccd701483045022100abf740b58d79cab000f8b0d328c2fff7eb88933971d1b63f8b99e89ca3f2dae602203354770db3cc2623349c87dea7a50cee1f78753141a5052b2d58aeb592bcf50f014cc9524104a882d414e478039cd5b52a92ffb13dd5e6bd4515497439dffd691a0f12af9575fa349b5694ed3155b136f09e63975a1700c9f4d4df849323dac06cf3bd6458cd41046ce31db9bdd543e72fe3039a1f1c047dab87037c36a669ff90e28da1848f640de68c2fe913d363a51154a0c62d7adea1b822d05035077418267b1a1379790187410411ffd36c70776538d079fbae117dc38effafb33304af83ce4894589747aee1ef992f63280567f52f5ba870678b4ab4ff6c8ea600bd217870a8b4f1f09f3a8e8353aeffffffff0130d90000000000001976a914569076ba39fc4ff6a2291d9ea9196d8c08f9c7ab88ac00000000'
        transaction = Transaction.parse(BytesIO(unhexlify(raw_transaction)))
        print(json.dumps(transaction.to_dict(), cls=ComplexEncoder, indent=2))
        # assert transaction.txid == '2fa5009216a99a9b4b93574eb274b7f64390dca654e7931506efe6c7ace91cc0'
        #
        raw_transaction = '010000000001016e263fd5f61d5d85f6a220c72bbea6c5f2fd7258ba49e622d97836929313be1d0000000000ffffffff0201c02c3a000000001600147f51134787005f1b667d3eccc187bc723538b096992719000000000017a914f778256e83c7b2e45194d166cf981a27e9553a29870247304402205361dc91b42e19e0082444001c249bfdbd3559a4d13ec04f02b799a816e269a30220366e7b34860705aebf80fdd3b4ccf7a99aad4e0092334d13060bf98b48dac12b012102439161ea5e23585bfbf1d20b6b540388dece80c37ea8a3c13bfb08ac99aeba6400000000'
        transaction = Transaction.parse(BytesIO(unhexlify(raw_transaction)))
        print(json.dumps(transaction.to_dict(), cls=ComplexEncoder, indent=2))


if __name__ == "__main__":
    unittest.main()
