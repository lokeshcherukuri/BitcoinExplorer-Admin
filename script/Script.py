from io import BytesIO
from Utilities import bytesToInt
from utils.EncoderDecoder import decodeToAscii
from .ScriptOpCodes import OP_CODES


class Script:

    def __init__(self, script_hex, script_decoded):
        self.hex = script_hex
        self.asm = script_decoded

    def __repr__(self):
        return '{{ \n hex: {}, \n asm: {} \n }}'.format(
            self.hex, self.asm
        )

    @classmethod
    def parse(cls, stream):
        stack = []
        script_hex = decodeToAscii(stream.getvalue())
        stack = cls.parseScript(stream, stack)
        script_decoded = ' '.join(str(element) for element in stack)
        return cls(script_hex, script_decoded.strip())

    @staticmethod
    def parseScript(stream, stack):
        current_byte = stream.read(1)
        while current_byte != b'':
            value = bytesToInt(current_byte)
            if value == 0:
                stack.append('00')
            elif 1 <= value <= 75:
                data = decodeToAscii(stream.read(value))
                if data.startswith('30') and data.endswith('01'):
                    data = data[:-2] + '[ALL]'
                stack.append(data)
            elif 76 <= value <= 78:
                if value == 76:
                    push_data_size = bytesToInt(stream.read(1))
                elif value == 77:
                    push_data_size = bytesToInt(stream.read(2))
                else:
                    push_data_size = bytesToInt(stream.read(4))
                push_data = stream.read(push_data_size)
                Script.parseScript(BytesIO(push_data), stack)
            elif value == 79:
                stack.append('-1')
            elif value == 81:
                stack.append('1')
            elif 82 <= value <= 96:
                stack.append(value - 80)
            else:
                stack.append(OP_CODES[value])

            current_byte = stream.read(1)

        return stack


