from Utilities import bytes_to_int
from binascii import hexlify
from .ScriptOpCodes import OP_CODES


class Script:
    def __init__(self, script_hex, script_decoded):
        self.hex = script_hex
        self.asm = script_decoded

    @classmethod
    def parse(cls, stream):
        current_position = stream.tell()
        script_hex = hexlify(stream.read()).decode('ascii')
        stream.seek(current_position)

        current_byte = stream.read(1)
        script_decoded = ''
        while current_byte != b'':
            value = bytes_to_int(current_byte)
            if value == 0:
                script_decoded += '00 '
            elif 1 <= value <= 75:
                script_decoded += stream.read(value) + ' '
            elif 76 <= value <= 78:
                if value == 76:
                    push_data_size = bytes_to_int(stream.read(1))
                elif value == 77:
                    push_data_size = bytes_to_int(stream.read(2))
                else:
                    push_data_size = bytes_to_int(stream.read(4))
                script_decoded += hexlify(stream.read(push_data_size)).decode('ascii') + ' '
            elif value == 79:
                script_decoded += '-1 '
            elif value == 81:
                script_decoded += '1 '
            elif 82 <= value <= 96:
                script_decoded += (value-80) + ' '
            else:
                script_decoded += OP_CODES[value]

            current_byte = stream.read(1)

        script_decoded = script_decoded.strip()
        return cls(script_hex, script_decoded)


