from django.test import TestCase
import unittest2
from .models import Bookings
from django.contrib.auth.models import User
from datetime import date, time


class TestDates(unittest2.TestCase):
    """
    Check Bookings.expired() function
    """

    def setUp(self):
        Bookings.objects.create(
            lesson='Theory',
            lesson_type='Offline',
            date='2030-10-24',
            time='12:00',
            student_id=1,
            status=True
            )
        Bookings.objects.create(
            lesson='Piano',
            lesson_type='Offline',
            date='2022-10-24',
            time='12:00',
            student_id=1,
            status=True
            )
        Bookings.expired()

    def test_dates(self):
        """
        Check if False is setting only to past date
        """
        fut = Bookings.objects.get(date='2030-10-24')
        past = Bookings.objects.get(date='2022-10-24')
        message_past = "Past date is True."
        message_fut = "Future date is False."
        self.assertFalse(past.status, message_past)
        self.assertTrue(fut.status, message_fut)
        past.delete()
        fut.delete()


class TestLesson(unittest2.TestCase):

    def setUp(self):
        Bookings.objects.create(
            lesson='Theory',
            lesson_type='Offline',
            date='2022-10-25',
            time='12:00',
            student_id=1,
            status=False
            )

    def test_lesson(self):
        """
        Check if Bookings values are returned correctly
        """
        lesson = Bookings.objects.get(date='2022-10-25')
        message_lesson = "Lesson is not Theory."
        message_lesson_type = "Lesson type is not Offline."
        message_date = "The date is not 2022-10-25."
        message_time = "Time is not 12:00."
        self.assertEqual(Bookings.get_lesson(lesson), 'Theory', message_lesson)
        self.assertEqual(
            Bookings.get_lesson_type(lesson),
            'Offline',
            message_lesson_type
            )
        self.assertEqual(
            Bookings.get_date(lesson),
            date(2022, 10, 25),
            message_date
            )
        self.assertEqual(Bookings.get_time(lesson), time(12, 0), message_time)
        lesson.delete()


if __name__ == '__main__':
    unittest.main()
