import unittest


class Singleton:

    instance = None

    def __new__(cls, value=None):
        if cls.instance is None:
            cls.instance = object.__new__(cls)
        cls.instance.value = value
        return cls.instance


# class TestSingleton(unittest.TestCase):
#     singleton = Singleton()
#     singleton.value = 'lokesh'
#     print(singleton.value)
#
#
# if __name__ == '__main__':
#     unittest.main()
