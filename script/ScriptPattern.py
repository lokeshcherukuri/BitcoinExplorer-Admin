from Globals import LEGACY_ADDRESS_SIZE, PKH_WITNESS_LENGTH, SH_WITNESS_LENGTH


class ScriptPattern:
    @staticmethod
    def findScriptType(script):
        elements = script.split(' ')
        if ScriptPattern.isPayToPubKey(elements):
            return 'pubkey'
        elif ScriptPattern.isPayToPubKeyHash(elements):
            return 'pubkeyhash'
        elif ScriptPattern.isPayToScriptHash(elements):
            return 'scripthash'
        elif ScriptPattern.isPayToWitnessPubKeyHash(elements):
            return 'witness_v0_keyhash'
        elif ScriptPattern.isPayToWitnessScriptHash(elements):
            return 'pay-to-witness-script-hash'
        elif ScriptPattern.isMultiSig(elements):
            return 'multisig'
        else:
            return 'Unknown Script Type'

    @staticmethod
    def isPayToPubKey(elements):
        if elements is None or len(elements) != 2:
            return False
        if elements[1] != 'OP_CHECKSIG':
            return False
        return True

    @staticmethod
    def isPayToPubKeyHash(elements):
        if elements is None or len(elements) != 5:
            return False
        if elements[0] != 'OP_DUP' or elements[1] != 'OP_HASH160':
            return False
        if elements[2] is None or len(elements[2]) != 2 * LEGACY_ADDRESS_SIZE:
            return False
        if elements[3] != 'OP_EQUALVERIFY':
            return False
        if elements[4] != 'OP_CHECKSIG':
            return False
        return True

    @staticmethod
    def isPayToScriptHash(elements):
        if elements is None or len(elements) != 3:
            return False
        if elements[0] != 'OP_HASH160':
            return False
        if elements[1] is None or len(elements[1]) != 2 * LEGACY_ADDRESS_SIZE:
            return False
        if elements[2] != 'OP_EQUAL':
            return False
        return True

    @staticmethod
    def isPayToWitnessPubKeyHash(elements):
        if elements is None or len(elements) != 2:
            return False
        if elements[0] is None or elements[0] != '00':
            return False
        if elements[1] is None or len(elements[1]) != 2 * PKH_WITNESS_LENGTH:
            return False
        return True

    @staticmethod
    def isPayToWitnessScriptHash(elements):
        if elements is None or len(elements) != 2:
            return False
        if elements[0] is None or elements[0] != '00':
            return False
        if elements[1] is None or len(elements[1]) != 2 * SH_WITNESS_LENGTH:
            return False
        return True

    @staticmethod
    def isMultiSig(elements):
        if elements is None or len(elements) < 4:
            return False
        last_ele = elements[len(elements)-1]
        if last_ele != 'OP_CHECKMULTISIG' and last_ele != 'OP_CHECKMULTISIGVERIFY':
            return False
        n = int(elements[0])
        if n < 1 or n > 16:
            return False
        m = int(elements[len(elements)-2])
        if m < 1 or m > 16:
            return False
        return True

    @staticmethod
    def getDestinationHashes(script, script_type):
        hashes = []
        if script is None:
            return RuntimeError("Script is Empty")
        elements = script.split(' ')
        if script_type == 'pubkeyhash':
            return [elements[2]]
        elif script_type == 'scripthash':
            return [elements[1]]
        else:
            # TODO implement for othe script types
            RuntimeError("Not Implemented")
            return []
