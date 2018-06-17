import json
import math
import unittest
from binascii import unhexlify
from io import BytesIO

from ComplexEncoder import ComplexEncoder
from Utilities import bytesToInt, varInt, readAndResetStream
from transaction.TransactionInput import TransactionInput
from transaction.TransactionOutput import TransactionOutput
from utils.Sha256Hash import doubleSha256
from utils.EncoderDecoder import decodeToAscii, switchEndianAndDecode


class Transaction:
    def __init__(self, txid, txhash, version, size, vsize, witnesslength, vin, vout, locktime):
        self.txid = txid
        self.hash = txhash
        self.version = version
        self.size = size
        self.vsize = vsize
        self.witnesslength = witnesslength
        self.vin = vin
        self.vout = vout
        self.locktime = locktime

    def __repr__(self):
        inputs = ''
        for tx_input in self.vin:
            inputs += tx_input.__repr__()

        outputs = ''
        for tx_output in self.vout:
            outputs += tx_output.__repr__()

        return '{{ \n txid:{}, \n hash:{}, \n version:{}, \n size:{}, \n vsize:{}, \n vin:[{}], \n vout:[{}], \n locktime:{} \n }}'.format(
            self.txid, self.hash, self.version, self.size, self.vsize, inputs, outputs, self.locktime
        )

    def toString(self):
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
        tx_start_position = stream.tell()
        tx_hash = switchEndianAndDecode(doubleSha256(stream.getvalue()))

        version_bytes = stream.read(4)
        version = bytesToInt(version_bytes)
        non_witness_bytes = version_bytes

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
        tx_end_position = stream.tell()

        tx_id = switchEndianAndDecode(doubleSha256(non_witness_bytes))
        size = tx_end_position - tx_start_position
        vsize = math.ceil((len(non_witness_bytes)*3 + size)/4)
        witnesslength = size - len(non_witness_bytes)

        return cls(tx_id, tx_hash, version, size, vsize, witnesslength, vin, vout, locktime)

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
        vin = [TransactionInput.parse(stream) for _ in range(vin_size)]
        return vin

    @staticmethod
    def parseTxOutputs(stream):
        vout_size = varInt(stream)
        vout = []
        for index in range(vout_size):
            tx_output = TransactionOutput.parse(stream)
            tx_output.output_index = index
            vout.append(tx_output)
        return vout

    @staticmethod
    def parseWitness(stream):
        witness_stack_size = varInt(stream)
        witness_stack = []
        for _ in range(witness_stack_size):
            witness_stack_item_len = varInt(stream)
            witness = decodeToAscii(stream.read(witness_stack_item_len))
            witness_stack.append(witness)
        return witness_stack


class TestTransaction(unittest.TestCase):
    def test_parse(self):
        # coinbase tx with pubkey output
        raw_transaction = '01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff08044c86041b020602ffffffff0100f2052a010000004341041b0e8c2567c12536aa13357b79a073dc4444acb83c4ec7a0e2f99dd7457516c5817242da796924ca4e99947d087fedf9ce467cb9f7c6287078f801df276fdf84ac00000000'
        transaction = Transaction.parse(BytesIO(unhexlify(raw_transaction)))
        assert transaction.txid == '8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87'
        print(json.dumps(transaction.toString(), cls=ComplexEncoder, indent=2))

        # pubkeyhash and scripthash outputs
        raw_transaction = '01000000017cc121bf0baf0a38b36697bb4d6a24edb13efb2ca7de277e8a7f7b015121f75c010000006a473044022071d4bb63c23ebcb70fe38d51731564199541ab3ad74ce2667488a932cb673333022059a235d87caaeb7b5786036a6d6debdcda5b20bb2f96dd7b43f039f2640f3c9401210375522818c3b28945fc4bde4a9429dcd8a4ef01fd7f7c2a1407306abc22e4c5d5feffffff025023bf1f000000001976a914e33a59763b5e008f8e20cb23c765fe7ed000b66188ac924344000000000017a914b549a78d07c2fa029eaa1b2b6effac8064e6a36f872fc80700'
        transaction = Transaction.parse(BytesIO(unhexlify(raw_transaction)))
        assert transaction.txid == '4e66a9188eca7e43c2d169d87f5b2319dc2c19726b8ba0af38adb88492f6a406'
        print(json.dumps(transaction.toString(), cls=ComplexEncoder, indent=2))

        # segwit tx with witness
        raw_transaction = '01000000000102d9028184f9dc166b4c59bafcaaf2a2a21440c832c7994e74a7871eb25aac386501000000171600144d9458205311924ff38df9096e55a68494613eb5ffffffffdb31fe7f8a9df2c7fd65720bd67a1977d94638464f7fa999309eb1976dd7e0fa01000000171600141f7765aed84e6afc0d67a699c126e7c4d38e2121ffffffff0280778e06000000001976a9141d0efca73a712e0116dfe77a20926aeb9378460488acdd28da590700000017a9144daba1dc5807d203253cf10ee55a751f85403a79870247304402200dae39e241bc21c389ae9da74d77bb12a4b26b704c198a994195c99324089fb80220363bae82fa825f25882353c81b1bf2715b62fe38cc6de0366e5ef0125ccbd1af01210256f76143ff6b467ee50bf3f35a83290b7ccbc17af055bfb1d53e465afb921bab02483045022100a3b0c314e67d7d22355181b36ab857a75652abbd74007909557048cf137ec98c0220574b7f895573c35b2f9bea6582b7ae5cf70f2d330ae83fe41cdf6b74e417af01012103d8271f9886f2c4be689f7bbf0f8b38a24b9ebd309d9f88cd4da4c2adc22c6dce00000000'
        transaction = Transaction.parse(BytesIO(unhexlify(raw_transaction)))
        assert transaction.txid == '058fc390bb3a966bc59a627af80a3139b407e50a6b24ce9b659841b87bd0f6a1'
        print(json.dumps(transaction.toString(), cls=ComplexEncoder, indent=2))

        # pay-to-witness-pubkey-hash  output
        raw_transaction = '010000000001016e263fd5f61d5d85f6a220c72bbea6c5f2fd7258ba49e622d97836929313be1d0000000000ffffffff0201c02c3a000000001600147f51134787005f1b667d3eccc187bc723538b096992719000000000017a914f778256e83c7b2e45194d166cf981a27e9553a29870247304402205361dc91b42e19e0082444001c249bfdbd3559a4d13ec04f02b799a816e269a30220366e7b34860705aebf80fdd3b4ccf7a99aad4e0092334d13060bf98b48dac12b012102439161ea5e23585bfbf1d20b6b540388dece80c37ea8a3c13bfb08ac99aeba6400000000'
        transaction = Transaction.parse(BytesIO(unhexlify(raw_transaction)))
        print(json.dumps(transaction.toString(), cls=ComplexEncoder, indent=2))
        assert transaction.txid == 'fbc8add6c1b01c4c5f78c86627e22cb769a17203cb87f62421013b3e4aeea185'

        # multisig outputs
        raw_transaction = '0100000001d8a037cb2af19424de458a3ae56e48487fe0682f829df4c27a5add2f6f4287b1030000006c493046022100d78c31a20fa11533475be893b229eb4d252e600dcc2a0735d360c541b6aec813022100e3eaa72c915ef47d94ccbd18c2ba6d9ae5b98be6e9fbf968d4bbbb003e06d6870121030e001332b43924be343986cca3df669f57b0dedd120990e727787f8dea50fdbcffffffff046c2a000000000000475121030e001332b43924be343986cca3df669f57b0dedd120990e727787f8dea50fdbc2120434e545250525459000000140001a9e0e85838b5000000174876e800010053b652ae6c2a000000000000475121030e001332b43924be343986cca3df669f57b0dedd120990e727787f8dea50fdbc2120a3c300000000000000000000000000000000000000000000000000000000000052ae6c2a000000000000475121030e001332b43924be343986cca3df669f57b0dedd120990e727787f8dea50fdbc2110000000000000000000000000000000000000000000000000000000000000000052aebc321000000000001976a914a2f2d251cc06ec1e789800127e3fa6ed9e51565188ac00000000'
        transaction = Transaction.parse(BytesIO(unhexlify(raw_transaction)))
        print(json.dumps(transaction.toString(), cls=ComplexEncoder, indent=2))
        assert transaction.txid == '055f9c6dc094cf21fa224e1eb4a54ee3cc44ae9daa8aa47f98df5c73c48997f9'

        # spending a multisig output with redeem script
        raw_transaction = '01000000013dcd7d87904c9cb7f4b79f36b5a03f96e2e729284c09856238d5353e1182b00200000000fd5d01004730440220762ce7bca626942975bfd5b130ed3470b9f538eb2ac120c2043b445709369628022051d73c80328b543f744aa64b7e9ebefa7ade3e5c716eab4a09b408d2c307ccd701483045022100abf740b58d79cab000f8b0d328c2fff7eb88933971d1b63f8b99e89ca3f2dae602203354770db3cc2623349c87dea7a50cee1f78753141a5052b2d58aeb592bcf50f014cc9524104a882d414e478039cd5b52a92ffb13dd5e6bd4515497439dffd691a0f12af9575fa349b5694ed3155b136f09e63975a1700c9f4d4df849323dac06cf3bd6458cd41046ce31db9bdd543e72fe3039a1f1c047dab87037c36a669ff90e28da1848f640de68c2fe913d363a51154a0c62d7adea1b822d05035077418267b1a1379790187410411ffd36c70776538d079fbae117dc38effafb33304af83ce4894589747aee1ef992f63280567f52f5ba870678b4ab4ff6c8ea600bd217870a8b4f1f09f3a8e8353aeffffffff0130d90000000000001976a914569076ba39fc4ff6a2291d9ea9196d8c08f9c7ab88ac00000000'
        transaction = Transaction.parse(BytesIO(unhexlify(raw_transaction)))
        print(json.dumps(transaction.toString(), cls=ComplexEncoder, indent=2))
        assert transaction.txid == '2fa5009216a99a9b4b93574eb274b7f64390dca654e7931506efe6c7ace91cc0'


if __name__ == "__main__":
    unittest.main()
