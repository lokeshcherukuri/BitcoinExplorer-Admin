from unittest import TestCase, main
from script.Script import Script


class ScriptSig(Script):
    def __init__(self, script_hex, script_decoded):
        super().__init__(script_hex, script_decoded)

    @staticmethod
    def to_dict(self):
        return dict(
            hex=self.hex,
            asm=self.asm
        )

    @classmethod
    def parse(cls, stream):
        script = Script.parse(stream)
        return script


class TestScriptSig(TestCase):
    def test_parse(self):
        print('testing script sig')


if __name__ == '__main__':
    main()