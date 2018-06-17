from unittest import TestCase, main


class TimetableRepository:

    INSERT_TIMETABLE = 'INSERT INTO timetable (name, lastupdated) VALUES (%(name)s, %(lastupdated)s)'
    FIND_BY_ID = 'SELECT * FROM timetable WHERE name = %(name)s'

    def __init__(self):
        pass

    def insert(self, timetable):
        pass

    def findByName(self, name):
        pass


class TestTimetableRepository(TestCase):

    def test_insert(self):
        pass

    def test_findByName(self):
        pass


if __name__ == '__main__':
    main()
