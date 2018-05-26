import requests


class Blockchain:
    def __init__(self):
        self.host = 'http://localhost:8333'

    def getBlockchaininfo(self, params):
        requestparams = {'jsonrpc': 2.0, 'id': 1, 'method': 'getblockchaininfo', 'params': params}
        request = requests.get(self.host, auth=('username', 'password'), params=requestparams)
        return request.json()

    def getMempoolInfo(self, params):
        requestparams = {'jsonrpc': 2.0, 'id': 1, 'method': 'getmempoolinfo', 'params': params}
        request = requests.get(self.host, auth=('username', 'password'), params=requestparams)
        return request.json()

    def getBlockHash(self, params):
        requestparams = {'jsonrpc': 2.0, 'id': 1, 'method': 'getblockhash', 'params': params}
        request = requests.get(self.host, auth=('username', 'password'), params=requestparams)
        return request.json()

    def getBlock(self, params):
        requestparams = {'jsonrpc': 2.0, 'id': 1, 'method': 'getblock', 'params': params}
        request = requests.get(self.host, auth=('username', 'password'), params=requestparams)
        return request.json()

    def getRawTransaction(self, params):
        requestparams = {'jsonrpc': 2.0, 'id': 1, 'method': 'getrawtransaction', 'params': params}
        request = requests.get(self.host, auth=('username', 'password'), params=requestparams)
        return request.json()

    def decodeRawTransaction(self, params):
        requestparams = {'jsonrpc': 2.0, 'id': 1, 'method': 'decoderawtransaction', 'params': params}
        request = requests.get(self.host, auth=('username', 'password'), params=requestparams)
        return request.json()
