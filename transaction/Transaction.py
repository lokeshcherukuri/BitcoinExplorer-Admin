import unittest
from io import BytesIO
from binascii import unhexlify
from ComplexEncoder import ComplexEncoder
from Utilities import bytesToInt, varInt, readAndResetStream
from transaction.TransactionInput import TransactionInput
from transaction.TransactionOutput import TransactionOutput
from Utilities import doubleSha256, decodeToAscii, switchEndianAndDecode
import math
import json


class Transaction:
    def __init__(self, txid, txhash, version, size, vsize, vin, vout, locktime):
        self.txid = txid
        self.hash = txhash
        self.version = version
        self.size = size
        self.vsize = vsize
        self.vin = vin
        self.vout = vout
        self.locktime = locktime

    def to_dict(self):
        return dict(
            txid=self.txid,
            hash=self.hash,
            version=self.version,
            size=self.size,
            vsize=self.vsize,
            locktime=self.locktime,
            vin=self.vin,
            vout=self.vout
        )

    @classmethod
    def parse(cls, stream):
        tx_hash = switchEndianAndDecode(doubleSha256(stream.getvalue()))

        version_bytes = stream.read(4)
        version = bytesToInt(version_bytes)
        non_witness_bytes = version_bytes

        size = len(stream.getvalue())
        is_tx_segwit = cls.isTxSegwit(stream)

        inputs_start_pos = stream.tell()
        vin = cls.parseTxInputs(stream)
        vout = cls.parseTxOutputs(stream)
        outputs_end_pos = stream.tell()
        non_witness_bytes += readAndResetStream(stream, outputs_end_pos, inputs_start_pos, outputs_end_pos)

        if is_tx_segwit:
            for tx_input in vin:
                txin_witness = cls.parseWitness(stream)
                tx_input.txinwitness = txin_witness

        locktime_bytes = stream.read(4)
        locktime = bytesToInt(locktime_bytes)
        non_witness_bytes = non_witness_bytes + locktime_bytes

        tx_id = switchEndianAndDecode(doubleSha256(non_witness_bytes))
        vsize = math.ceil((len(non_witness_bytes)*3 + size)/4)

        return cls(tx_id, tx_hash, version, size, vsize, vin, vout, locktime)

    @staticmethod
    def isTxSegwit(stream):
        reset_stream_pos = stream.tell()
        marker = bytesToInt(stream.read(1))
        if marker != 0x00:
            stream.seek(reset_stream_pos)
            return False
        flag = bytesToInt(stream.read(1))
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
            witness_stack_item_len = varInt(stream)
            witness = decodeToAscii(stream.read(witness_stack_item_len))
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
        assert transaction.txid == '4e66a9188eca7e43c2d169d87f5b2319dc2c19726b8ba0af38adb88492f6a406'
        print(json.dumps(transaction.to_dict(), cls=ComplexEncoder, indent=2))

        # segwit tx with witness
        raw_transaction = '01000000000102d9028184f9dc166b4c59bafcaaf2a2a21440c832c7994e74a7871eb25aac386501000000171600144d9458205311924ff38df9096e55a68494613eb5ffffffffdb31fe7f8a9df2c7fd65720bd67a1977d94638464f7fa999309eb1976dd7e0fa01000000171600141f7765aed84e6afc0d67a699c126e7c4d38e2121ffffffff0280778e06000000001976a9141d0efca73a712e0116dfe77a20926aeb9378460488acdd28da590700000017a9144daba1dc5807d203253cf10ee55a751f85403a79870247304402200dae39e241bc21c389ae9da74d77bb12a4b26b704c198a994195c99324089fb80220363bae82fa825f25882353c81b1bf2715b62fe38cc6de0366e5ef0125ccbd1af01210256f76143ff6b467ee50bf3f35a83290b7ccbc17af055bfb1d53e465afb921bab02483045022100a3b0c314e67d7d22355181b36ab857a75652abbd74007909557048cf137ec98c0220574b7f895573c35b2f9bea6582b7ae5cf70f2d330ae83fe41cdf6b74e417af01012103d8271f9886f2c4be689f7bbf0f8b38a24b9ebd309d9f88cd4da4c2adc22c6dce00000000'
        transaction = Transaction.parse(BytesIO(unhexlify(raw_transaction)))
        assert transaction.txid == '058fc390bb3a966bc59a627af80a3139b407e50a6b24ce9b659841b87bd0f6a1'
        print(json.dumps(transaction.to_dict(), cls=ComplexEncoder, indent=2))

        raw_transaction = '01000000013dcd7d87904c9cb7f4b79f36b5a03f96e2e729284c09856238d5353e1182b00200000000fd5d01004730440220762ce7bca626942975bfd5b130ed3470b9f538eb2ac120c2043b445709369628022051d73c80328b543f744aa64b7e9ebefa7ade3e5c716eab4a09b408d2c307ccd701483045022100abf740b58d79cab000f8b0d328c2fff7eb88933971d1b63f8b99e89ca3f2dae602203354770db3cc2623349c87dea7a50cee1f78753141a5052b2d58aeb592bcf50f014cc9524104a882d414e478039cd5b52a92ffb13dd5e6bd4515497439dffd691a0f12af9575fa349b5694ed3155b136f09e63975a1700c9f4d4df849323dac06cf3bd6458cd41046ce31db9bdd543e72fe3039a1f1c047dab87037c36a669ff90e28da1848f640de68c2fe913d363a51154a0c62d7adea1b822d05035077418267b1a1379790187410411ffd36c70776538d079fbae117dc38effafb33304af83ce4894589747aee1ef992f63280567f52f5ba870678b4ab4ff6c8ea600bd217870a8b4f1f09f3a8e8353aeffffffff0130d90000000000001976a914569076ba39fc4ff6a2291d9ea9196d8c08f9c7ab88ac00000000'
        transaction = Transaction.parse(BytesIO(unhexlify(raw_transaction)))
        print(json.dumps(transaction.to_dict(), cls=ComplexEncoder, indent=2))
        assert transaction.txid == '2fa5009216a99a9b4b93574eb274b7f64390dca654e7931506efe6c7ace91cc0'

        raw_transaction = '010000000001016e263fd5f61d5d85f6a220c72bbea6c5f2fd7258ba49e622d97836929313be1d0000000000ffffffff0201c02c3a000000001600147f51134787005f1b667d3eccc187bc723538b096992719000000000017a914f778256e83c7b2e45194d166cf981a27e9553a29870247304402205361dc91b42e19e0082444001c249bfdbd3559a4d13ec04f02b799a816e269a30220366e7b34860705aebf80fdd3b4ccf7a99aad4e0092334d13060bf98b48dac12b012102439161ea5e23585bfbf1d20b6b540388dece80c37ea8a3c13bfb08ac99aeba6400000000'
        transaction = Transaction.parse(BytesIO(unhexlify(raw_transaction)))
        print(json.dumps(transaction.to_dict(), cls=ComplexEncoder, indent=2))
        assert transaction.txid == 'fbc8add6c1b01c4c5f78c86627e22cb769a17203cb87f62421013b3e4aeea185'

        raw_transaction = '01000000000107431ee8ed1d660bd9b5163d6379cd2439aa6d259a14096996ae4bdb6953aea9650100000023220020d2c698bb72ade09ea873fa3c50c28332b42507c76c1f05bc2ede0af53f500010fdffffffb2908958511215a95278339d0d79d2c87d918e9f8b0d932477a03c8023b5ff33010000002322002035fdca1845a4f0b34843576f783e033a9b57732d281d4a8abcbd207d243db9b2fdffffffeb8d921457b6ec70af150f61a101a15be0b36df01a7e910ecf3a885450dbcd7701000000232200202330db9ac709392d73bbe46a005eace68212955dd55ff66b8f8661820399128ffdffffff685fd5a3de0521648968f55cd6bfb3601c0815bfe0431eeb8484fe9d74d7ca260100000023220020ea58c944a84902cdfc9cdaee13c3f1f9fdbb01e7a2c27476bc95c0fbfa27788dfdffffff3d4c0aa4d71cad6aedb9673588a2fb38adb217e02978ce86136c1d6c71a7884a63000000232200202fc0c6354a4d0cd9c3d680448f49ad0ce41bf6e18a1e09c4407145246757b952fdffffffa9a9c537e87716d41c0bfbbe460cc60035d262c01bcfeaa430ab88daec62bae20100000023220020871af08b1bd1cfd8b9986cc1aac7ba6a2f61c72277e26bc66b963fd034536eabfdffffff788ea275c444c7dd41fce3ab581b00496c8bd25b8141ce5c1e083cbcfb0ab3610000000023220020a0032951a458bbfc05e89ed677e1840deaa1af90aff60b4549eaa6f03dc5e9fffdffffff02a40600000000000017a914000abd6df9cce136a3b3535b73357b85772ecbbd8710f102010000000017a914748ac81fc6b858c65a0819ba8d8fb5b18e27ff5b870400483045022100c39d96d9e5b1ac5aa485b3f90c6e46b9b87c8b1b61487bb74c28bd8d61c59681022002a2773bcef20ec7627c65a8ce54f5b5f7563718bcec3e89d30b7a5634d03cb90147304402201848820785f4dda1eaf88e87f389c3f8a78dba7808430f081b1f8c11d667658902207b6a9a5774ada160c8ec26b8541b35b272ada59ebd3f4af17f2d39d418b83bce010102040047304402200f9dbd668672337e1dab24c92a85432e1225b2d3c1b79f8af62cdc3f971fa3e2022058ec4a50b923a3dcf01a0485e63a66e97fcc587de4418271b37a0b60d541f87301483045022100ca88dbe60f9d37346d33e7d789ebb25a202bd28b26006039cc4e667622afc7a1022011e0531a99adf2afca350c9a6735d95805bab3ab55a67d79c0e918d2814c32980101020400483045022100cc1552d76f6fcf4a04a8f65036b1f22925189660e63e524f416a3179313ddb690220097ee71fb584770bf607c80d1506b2e046d3e44636d7dde368d800752f095d8f01473044022059b19abb59f0b03a63352d57897afbc9a880489f2ea0092da293db9920ead1270220199b3b453d0e8b7ef4e3b7e920f478f36d3160a16b3923d2209f9af5b21078c9010102040047304402204851e816425a2a4885308a3cfa43dee3db91aaab1fbe3e7f7fb1d9083c00dcac02200822034f8bf77de00f52af940f3de86912478e30ee0db3d86e82f23b708f5bab014730440220578a25b70115c60247213538670579d11e12be25553fc12833199f520b0698d40220422a23fd557d1199dbe6f6d7cf2bc7f969299042b20ac0ef32a1d985f2819dd80101020400483045022100e7a9b0812a57c5982e7f3db2899ebb7f302bff165da63e87df42d80f6515a88202204f6cacb81aa5c6412c59a259d667e821f8e41829145c5b68953f7b8db6d1ce980147304402203dae20860837947d15bf776ab730b556eb675f09c8f6dafa021f4add1bce4d9302206d43cd3bb1cc112133d1eb00ead2861710f006e7a5e5f49d162259ad01bc828d0101020400483045022100bb9e40777b8fe45994554aa2e0a6bbdccb1b3f0690425b772d43fb4e9b4c54b802207f5bc7c28d34a95c623dae9724f2fac96dd9aab06d34fea45c3fd1977a911cd901473044022040d9c1614b9af2e192b4120b568dbb3a9ae8f953ccc71ccf977462e04f29e72d02201a5d9fc4fe65430d8189cff998670a7659c0420d2213942e7288455977abc8180101020400483045022100f276986b21455692f00226c4cba2f754191906fa931cd665db9b44ff9b19a1170220174e17dc9debbb6ccbf53fdcb94980add092a390422a8e636e5e6c0b7e90aee00147304402203af294578122bc4342e0a790088345f9c0fd5d349f74f12e6b27f4945d914838022064d6bdff11999c8334b02008cec4ea7ae8a80e2fab99655b8a01bc244c942dfd01010200000000'
        transaction = Transaction.parse(BytesIO(unhexlify(raw_transaction)))
        print(json.dumps(transaction.to_dict(), cls=ComplexEncoder, indent=2))
        assert transaction.txid == 'bb6b0bde5ae0e4ddf5083c39360ac5f54f3212f7996a38c9045097a75587290c'


if __name__ == "__main__":
    unittest.main()
