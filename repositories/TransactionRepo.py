import mysql.connector


class TransactionRepo:

    INSERT_TRANSACTION = "INSERT INTO transaction(txid, txhash, version, size, vsize, locktime, fees, confirmations) " \
                         "VALUES(%(txid)s, %(txhash)s, %(version)s, %(size)s, %(vsize)s, %(locktime)s, %(fees)s, %(confirmations)s)"

    connection = None

    def __init__(self):
        self.connection = mysql.connector.connect(user='lcherukuri', password='password',
                                                  host='127.0.0.1', database='test',
                                                  auth_plugin='mysql_native_password')
        pass

    def save(self, transaction):
        pass
