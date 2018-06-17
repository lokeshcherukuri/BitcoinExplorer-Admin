import json

import requests
from unittest import TestCase, main


class Blockchain:
    def __init__(self):
        self.host = 'http://username:password@192.168.86.87:18332'

    def query(self, method, params):
        if method is None:
            return RuntimeError("Invalid method name")
        if params is None:
            return RuntimeError("params are expected to be an Array")
        requestparams = {'jsonrpc': 2.0, 'id': 1, 'method': method, 'params': params}
        request = requests.post(self.host, data=json.dumps(requestparams))
        response = request.json()
        return response['result'] if response['error'] is None else None

    def getBlockchainInfo(self, params):
        return self.query('getblockchaininfo', params)

    def getMiningInfo(self, params):
        return self.query('getmininginfo', params)

    def getMempoolInfo(self, params):
        return self.query('getmempoolinfo', params)

    def getBlockHash(self, params):
        return self.query('getblockhash', params)

    def getBlock(self, params):
        return self.query('getblock', params)

    def getRawTransaction(self, params):
        return self.query('getrawtransaction', params)

    def decodeRawTransaction(self, params):
        return self.query('decoderawtransaction', params)


class BlockchainTest(TestCase):
    def test_getBlockchaininfo(self):
        print(Blockchain().getBlockchainInfo([]))


if __name__ == "__main__":
    main()
