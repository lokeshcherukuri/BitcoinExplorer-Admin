from .Address import Address


class SegwitAddress(Address):
    def __init__(self, address=None):
        super().__init__(address)

    @classmethod
    def fromWitnessHash(cls, witnesshash):
        # TODO Currently pay-to-witness-hash doesnt support addresses
        return None
