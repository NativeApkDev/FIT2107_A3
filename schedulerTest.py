import unittest
from unittest.mock import Mock, MagicMock, patch
from scheduler import Scheduler
from scheduler import IllegalArgumentException
from datetime import datetime


class SchedulerTest(unittest.TestCase):
    '''Tests for the scheduler class.  Add more tests
    to test the code that you write'''

    def setUp(self):
        self.scheduler = Scheduler()

    def test_itsalive(self):
        """ Testing find_time function to ensure that find_time function works correctly. """
        (stime, satellites) = self.scheduler.find_time(start_time=datetime(2018, 10, 12, 8, 0, 0, 0), duration=10,
                                                       n_windows=2)
        self.assertTrue(type(stime) == type(datetime.now()))

    def test_exceptionthrown(self):
        with self.assertRaises(IllegalArgumentException):
            """ Testing with start_time as the only argument of find_time function and start_time as a
            non-datetime object. """
            (stime, satellites) = self.scheduler.find_time(start_time = "now")

    def test_black_id_1(self):  # test case from black box method
        with self.assertRaises(IllegalArgumentException):
            """ Testing find_time function by using satlist_url which is a url string, start_time which is a 
            non-datetime object, n_windows which is a non-integer, duration which is an integer, sample_interval which 
            is a non-integer, cumulative as False, and location as a string instead of (latitude, longitude) tuple 
            (invalid argument). """
            (time, satellites) = self.scheduler.find_time(satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
                                                          start_time='2 am 10th October 2018', n_windows='three',
                                                          duration=60, sample_interval='three', cumulative=False,
                                                          location='monash university')

    def test_black_id_2(self):  # test case from black box method
        with self.assertRaises(IllegalArgumentException):
            """ Testing find_time function by using satlist_url as a random string, start_time as a datetime object,
            n_windows as an integer, duration as a non-integer, sample_interval as an integer, cumulative as a string
            saying "False" (which is an invalid argument), and location as a (latitude, longitude) tuple. """
            (time, satellites) = self.scheduler.find_time(satlist_url='a random string',
                                                          start_time=datetime(2018, 10, 12, 8, 0, 0, 0), n_windows=3,
                                                          duration='asd', sample_interval=3, cumulative='False',
                                                          location=(-37.910496,145.134021))

    def test_black_id_3(self):  # test case from black box method
        with self.assertRaises(IllegalArgumentException):
            """ Testing find_time function by using satlist_url as a non-string, start_time as a datetime object,
            n_windows as an integer, duration as an integer, sample_interval as an integer, cumulative as True,
            and location as a string instead of a (latitude, longitude) tuple (invalid argument). """
            (time, satellites) = self.scheduler.find_time(satlist_url=12,start_time=datetime(2018, 10, 12, 8, 0, 0, 0),
                                                          n_windows=3, duration=60, sample_interval=3, cumulative=True,
                                                          location='monash university')

    def test_black_id_4(self):  # test case from black box method
        with self.assertRaises(IllegalArgumentException):
            """ Testing find_time function by using satlist_url as a random string, start_time as a non-datetime object,
            n_windows as a non_integer, duration as a non-integer, sample_interval as a non-integer, cumulative as True,
            and location as a (latitude, longitude) tuple. """
            (time, satellites) = self.scheduler.find_time(satlist_url='a random string',
                                                          start_time='2 am 10th October 2018', n_windows='three',
                                                          duration='asd', sample_interval='three', cumulative=True,
                                                          location=(-37.910496,145.134021))

    def test_black_id_5(self):  # test case from black box method
        with self.assertRaises(IllegalArgumentException):
            """ Testing find_time function by using satlist_url as a url string, start_time as a datetime object,
            n_windows as a non-integer, duration as a non-integer, sample_interval as an integer, cumulative as False,
            and location as a (latitude, longitude) tuple. """
            (time, satellites) = self.scheduler.find_time(satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
                                                          start_time=datetime(2018, 10, 12, 8, 0, 0, 0),
                                                          n_windows='three', duration='asd', sample_interval=3,
                                                          cumulative=False, location=(-37.910496,145.134021))

    def test_black_id_6(self):  # test case from black box method
        with self.assertRaises(IllegalArgumentException):
            """ Testing find_time function by using satlist_url as a non_string, start_time as a non-datetime object,
            n_windows as a non-integer, duration as an integer, sample_interval as a non-integer, cumulative as a
            string saying "False" (an invalid argument), and location as a (latitude, longitude) tuple. """
            (time, satellites) = self.scheduler.find_time(satlist_url=12, start_time='2 am 10th October 2018',
                                                          n_windows='three', duration=60, sample_interval='three',
                                                          cumulative='False', location=(-37.910496,145.134021))

    def test_black_id_7(self):  # test case from black box method
        with self.assertRaises(IllegalArgumentException):
            """ Testing find_time function by using satlist_url as a url string, start_time as a non-datetime object,
            n_windows as an integer, duration as a non-integer, sample_interval as an integer, cumulative as a string
            saying "False" (an invalid argument), and location as a string instead of a (latitude, longitude) tuple
            (invalid argument). """
            (time, satellites) = self.scheduler.find_time(satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
                                                          start_time='2 am 10th October 2018', n_windows=3,
                                                          duration='asd', sample_interval=3, cumulative='False',
                                                          location='monash university')

    def test_black_id_8(self):  # test case from black box method
        with self.assertRaises(IllegalArgumentException):
            """ Testing find_time function by using satlist_url as a random string, start_time as a datetime object,
            n_windows as an integer, duration as an integer, sample_interval as a non-integer, cumulative as False,
            and location as a string instead of a (latitude, longitude) tuple (invalid argument). """
            (time, satellites) = self.scheduler.find_time(satlist_url='a random string',
                                                          start_time=datetime(2018, 10, 12, 8, 0, 0, 0),
                                                          n_windows=3, duration=60, sample_interval='three',
                                                          cumulative=False, location='monash university')

    def test_black_id_9(self):  # test case from black box method
        with self.assertRaises(IllegalArgumentException):
            """ Testing find_time function by using satlist_url as a non-string, start_time as a datetime object,
            n_windows as an integer, duration as a non-integer, sample_interval as an integer, cumulative as False,
            and location as a string instead of a (latitude, longitude) tuple (invalid argument). """
            (time, satellites) = self.scheduler.find_time(satlist_url=12,
                                                          start_time=datetime(2018, 10, 12, 8, 0, 0, 0),
                                                          n_windows=3, duration='asd', sample_interval=3,
                                                          cumulative=False, location='monash university')

    def test_black_id_10(self):  # test case from black box method
        with self.assertRaises(IllegalArgumentException):
            """ Testing find_time function by using satlist_url as a url string, start_time as a non-datetime object,
            n_windows as a non-integer, duration as a non-integer, sample_interval as a non-integer, cumulative as
            True, and location as a (latitude, longitude) tuple. """
            (time, satellites) = self.scheduler.find_time(satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
                                                          start_time='2 am 10th October 2018', n_windows='three',
                                                          duration='asd', sample_interval='three', cumulative=True,
                                                          location=(-37.910496, 145.134021))

    def test_white_id_1(self):  # test case from white box method
        with self.assertRaises(IllegalArgumentException):
            """ Testing find_time function by using satlist_url as a url string, start_time as a non-datetime object,
            n_windows as a non-integer, duration as a non-integer, sample_interval as a non-integer, cumulative as
            True, and location as a (latitude, longitude) tuple. """
            (time, satellites) = self.scheduler.find_time(satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
                                                          start_time='2 am 10th October 2018', n_windows='three',
                                                          duration=60, sample_interval=3, cumulative=True,
                                                          location=(-37.910496, 145.134021))
    def test_white_id_2(self):  # test case from white box method
        """ Testing find_time function by using satlist_url as a url string, start_time as a non-datetime object,
        n_windows as a non-integer, duration as a non-integer, sample_interval as a non-integer, cumulative as
        True, and location as a (latitude, longitude) tuple. """
        (time, satellites) = self.scheduler.find_time(satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
                                                      start_time=datetime(2018, 10, 12, 8, 0, 0, 0),
                                                      n_windows=2, duration=10, sample_interval=1, cumulative=False,
                                                      location=(-37.910496, 145.134021))
        self.assertTrue(type(time) == type(datetime.now()))

    def test_white_id_3(self):  # test case from white box method
        """ Testing find_time function by using satlist_url as a url string, start_time as a non-datetime object,
        n_windows as a non-integer, duration as a non-integer, sample_interval as a non-integer, cumulative as
        True, and location as a (latitude, longitude) tuple. """
        (time, satellites) = self.scheduler.find_time(satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
                                                      start_time=datetime(2018, 10, 12, 8, 0, 0, 0),
                                                      n_windows=2, duration=10, sample_interval=1, cumulative=True,
                                                      location=(-37.910496, 145.134021))
        self.assertTrue(type(time) == type(datetime.now()))

    @patch('scheduler.positionlib.Apparent.altaz')  # Using patch to mock dummy data
    def test_white_id_4(self, mockTuple):  # test case from white box method
        mockTuple.return_value = (Mock(degrees=-1), 1, 1)
        """ Testing find_time function by using satlist_url as a url string, start_time as a datetime object, n_windows
        as an integer, duration as an integer, sample_interval as an integer, cumulative as False, and location as
        a (latitude, longitude tuple). """
        (time, satellites) = self.scheduler.find_time(satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
                                                      start_time=datetime(2018, 10, 12, 8, 0, 0, 0),
                                                      n_windows=2, duration=10, sample_interval=1, cumulative=False,
                                                      location=(-37.910496, 145.134021))
        self.assertEqual(satellites, [])


if __name__=="__main__":
    unittest.main()