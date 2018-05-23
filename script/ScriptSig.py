import json
from binascii import unhexlify
from io import BytesIO
from unittest import TestCase, main
from ComplexEncoder import ComplexEncoder
from script.Script import Script


class ScriptSig(Script):
    def __init__(self, script_hex, script_decoded):
        super().__init__(script_hex, script_decoded)

    def __repr__(self):
        return '{{ \n hex: {}, \n asm: {} \n }}'.format(
            self.hex, self.asm
        )

    def toString(self):
        return dict(
            hex=self.hex,
            asm=self.asm
        )

    @classmethod
    def parse(cls, stream):
        script = super().parse(stream)
        return script


class TestScriptSig(TestCase):
    def test_parse(self):
        script_hex = '004730440220762CE7BCA626942975BFD5B130ED3470B9F538EB2AC120C2043B445709369628022051D73C80328B543F744AA64B7E9EBEFA7ADE3E5C716EAB4A09B408D2C307CCD701483045022100ABF740B58D79CAB000F8B0D328C2FFF7EB88933971D1B63F8B99E89CA3F2DAE602203354770DB3CC2623349C87DEA7A50CEE1F78753141A5052B2D58AEB592BCF50F014CC9524104A882D414E478039CD5B52A92FFB13DD5E6BD4515497439DFFD691A0F12AF9575FA349B5694ED3155B136F09E63975A1700C9F4D4DF849323DAC06CF3BD6458CD41046CE31DB9BDD543E72FE3039A1F1C047DAB87037C36A669FF90E28DA1848F640DE68C2FE913D363A51154A0C62D7ADEA1B822D05035077418267B1A1379790187410411FFD36C70776538D079FBAE117DC38EFFAFB33304AF83CE4894589747AEE1EF992F63280567F52F5BA870678B4AB4FF6C8EA600BD217870A8B4F1F09F3A8E8353AE'
        script = ScriptSig.parse(BytesIO(unhexlify(script_hex)))
        print(json.dumps(script.toString(), cls=ComplexEncoder, indent=2))


if __name__ == '__main__':
    main()