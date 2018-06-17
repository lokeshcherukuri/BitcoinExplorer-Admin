from models.TimeTable import TimeTable
from repositories import TimeTableRepository
from unittest import TestCase, main


class TimetableService:

    def __init__(self):
        self.timeTableRepository = TimeTableRepository()

    def save(self, name, lastupdated):
        timetable = TimeTable(name, lastupdated)
        self.timeTableRepository.insert(timetable)

    def getByName(self, name):
        timetable = self.timeTableRepository.findByName(name)
        return timetable

    def reset(self, name):
        pass


class TestTimetableRepository(TestCase):
    def test_insert(self):
        pass

    def test_findByName(self):
        pass


if __name__ == '__main__':
    main()
