from unittest import TestCase, main


class BlockRepository:

    def __init__(self):
        pass

    def save(self):
        pass

    def findById(self, block_id):
        pass

    def findLatest(self, limit=5):
        pass


class TestBlockRepository(TestCase):

    def test_save(self):
        pass

    def test_findById(self):
        pass

    def test_findLatest(self):
        pass


if __name__ == '__main__':
    main()
