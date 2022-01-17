'''A class to calculate optimal times for satellite spotting
Initial skeleton code written by Robert Merkel for FIT2107 Assignment 3
'''
from skyfield import positionlib
from skyfield.api import Loader, Topos, load, Angle
import datetime, time
from datetime import datetime
from datetime import timedelta
from pytz import timezone


class IllegalArgumentException(Exception):
    '''An exception to throw if somebody provides invalid data to the Scheduler methods'''
    pass


class Scheduler:
    '''The class for calculating optimal satellite spotting times.  You can and should add methods
    to this, but please don't change the parameter list for the existing methods.  '''
    def __init__(self):
        '''Constructor sets things to put downloaded data in a sensible location. You can add
        to this if you want.  '''
        self._skyload = Loader('~/.skyfield-data')
        self.ts = self._skyload.timescale()


    def find_time(self, satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
    start_time=datetime.now(), n_windows=24, duration=60, sample_interval=1, cumulative=False,
    location=(-37.910496,145.134021)):
        '''NOTE: this is the key function that you'll need to implement for the assignment.  Please
        don't change the arguments.
        arguments: satlist_url (string) a URL to a file containing a list of Earth-orbiting
        satellites in TLE format)
                      start_time: a Python Datetime object representing the
                      the start of the potential observation windows,return

                      duration: the size (in minutes) of an observation window - must be positive
                      n_windows: the number of observation windows to check.  Must be a positive integer
                      sample_interval: the interval (in minutes) at which the visible
                      satellites are checked.  Must be smaller than duration.
                      cumulative: a boolean to determine whether we look for the maximum number
                      of satellites visible at any time within the duration (if False), or the
                      cumulative number of distinct satellites visible over the duration (if True)
                      location: a tuple (lat, lon) of floats specifying he latitude and longitude of the
                      observer.  Negative latitudes specify the southern hemisphere, negative longitudes
                      the western hemisphere.  lat must be in the range [-90,90], lon must be in the
                      range [-180, 180]
        returns:a tuple ( interval_start_time, satellite_list), where start_interval is
        the time interval from the set {(start_time, start_time + duration),
        (start_time + duration, start_time + 2*duration)...} with the most satellites visible at some
        point in the interval, or the most cumulative satellites visible over the interval (if cumulative=True)
        See the assignment spec sheet for more details.
        raises: IllegalArgumentException if an illegal argument is provided'''

        try:
            self.test_inputs(start_time=start_time, satlist_url=satlist_url, n_windows=n_windows, duration=duration,
                             location=location, sample_interval=sample_interval, cumulative=cumulative)
        except:
            raise IllegalArgumentException("Invalid argument")

        if cumulative is False:
            result = self.getIntervalWithHighestMaximum(start_time=start_time, satlist_url=satlist_url,
                                                        n_windows=n_windows, duration=duration,
                                                        location=location, sample_interval=sample_interval)
        else:
            result = self.getIntervalWithHighestTotal(start_time=start_time, satlist_url=satlist_url,
                                                      n_windows=n_windows, duration=duration,
                                                      location=location, sample_interval=sample_interval)
        sat_list = []
        for i in range(len(result[0])):
            sat_list.append(result[0][i].name)

        return (start_time, sat_list)

    def test_inputs(self, satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
    start_time=datetime.now(), n_windows=24, duration=60, sample_interval=1, cumulative=False,
    location=(-37.910496,145.134021)):
        '''
        A function to test if the inputs will raise an error or not
        :param satlist_url: the url to get the list of satellites
        :param start_time: the starting time
        :param n_windows: the number of windows / how many times the duration is repeated
        :param duration: a numerical value in minutes
        :param sample_interval: the interval / tick
        :param location: the user location
        :param cumulative: a True or False Boolean
        '''
        # If the input of cumulative is invalid
        if cumulative is not True and cumulative is not False:
            raise IllegalArgumentException("Invalid argument")
        if sample_interval >= duration:
            raise IllegalArgumentException("The sample interval must be lower than the duration")
        if isinstance(n_windows, type(1)) is False:
            raise IllegalArgumentException("Invalid argument")
        test = self.get_visibility(time=start_time, satlist_url=satlist_url, cumulative=cumulative, location=location)

    def getUTCtz(self, time):
        '''
        This function converts the timezone from GMT+8 to UTC
        :param time: time in GMT+8 timezone format
        :return: utc_time (time in UTC format)
        '''
        local_timezone = timezone('Asia/Kuala_Lumpur')
        newTime = local_timezone.localize(time)
        utc_time = self.ts.utc(newTime)
        return utc_time

    def get_visibility(self, time=datetime.now(), seen_sat=[], satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
    cumulative=False, location=(-37.910496,145.134021)):
        '''
        This function retrieves the list of satellites visible at a given time, assuming the time is local Malaysia Time
        :param time: a datetime object, assuming the default timezone as local Malaysia time or GMT+8
        :param vis_sat: a list of satellites that has been encountered, to check for unique satellites
        :param satlist_url: a url to get the list of satellites
        :param cumulative: Boolean True or False
        :param location: Location of the user
        :return: a list of the visible satellites
        '''
        if isinstance(time, datetime) is False:  # If time is not a datetime object, raise exception
            raise IllegalArgumentException('Incorrect arguments')

        time = self.getUTCtz(time)  # Assuming that the time inputted is of Malaysia Time

        sats = load.tle(satlist_url)  # Getting the list of satellites

        myLocation = Topos(location[0], location[1])  # Creating a Topos object containing the user location
        visible_satellites = []  # a list that will contain the visible satellites and be returned

        # Iterating through each satellite in sats and determining the visibility of each of the satellites
        for satellites in sats:
            # Calculating the values of the attributes of the satellite
            satellite = sats[satellites]  # Getting the satellite

            diff = satellite - myLocation  # Creating a vector
            coordinates = diff.at(time)  # Calculate the vector
            alt, az, distance = positionlib.Apparent.altaz(coordinates)  # Getting the altitude

            # Checking the elevation component of the position of the satellite
            # If the elevation component of the position of the satellite is greater than 0 degrees
            if alt.degrees > 0:  # The satellite is visible since it is above the horizon
                if cumulative is True:
                    if satellite in seen_sat: # If the satellite has been viewed before
                        continue
                    # Else if the satellite has not been visible before
                    else:
                        visible_satellites.append(satellite)  # Append the satellite into the list
                        seen_sat.append(satellite)
                else:
                    visible_satellites.append(satellite)

        return visible_satellites

    def getMaxNumOfSatellitesVisible(self, satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
    start_time=datetime.now(), duration=60, sample_interval=1, location=(-37.910496,145.134021)):
        '''
        This function gets the maximum number of satellites visible over a given time interval
        :param satlist_url: the satellite url to get the list of satellites
        :param start_time: the starting time, a datetime object
        :param duration: a numerical value in minutes
        :param sample_interval: the interval / tick
        :param location: the location of the user
        :return: a tuple containing the list of satellite and the time
        '''
        # The sample interval must be lower than the duration
        current_time = start_time  # Creating another datetime object to keep track of time
        list_of_satellites = []  # List containing another list of satellites
        # While the tracking time is still under the starting time + duration
        while current_time <= start_time + timedelta(minutes=duration):
            # Get the visible satellite at the current time
            visible_satellites = self.get_visibility(time=current_time, satlist_url=satlist_url, location=location)
            # Append the list into another list
            list_of_satellites.append(visible_satellites)

            # Add the value of current_time by sample_interval (the length of the subinterval)
            current_time += timedelta(minutes=sample_interval)

        # Getting the value of the maximum number of satellites visible and the index
        max = 0
        index = 0
        for i in range(len(list_of_satellites)):
            if len(list_of_satellites[i]) > max:
                max = len(list_of_satellites[i])
                index = i
        # Calculate the time when the num of satellite is at peak
        total_interval = sample_interval * index
        the_time = start_time + timedelta(minutes=total_interval)
        return (list_of_satellites[index], the_time)

    def getTotalNumOfSatellitesVisible(self, satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
    start_time=datetime.now(), duration=60, sample_interval=1, location=(-37.910496, 145.134021), seen_sats=[]):
        '''
        This function gets to highest number of unique satellites over a duration of time
        :param satlist_url: the satellite url to get the list of satellites
        :param start_time: the starting time, a datetime object
        :param duration: a numerical value in minutes
        :param sample_interval: the interval / tick
        :param location: the location of the user
        :param seen_sats: a list that is used to check if the satellite is unique or not
        :return: a tuple containing the list of satellite and the time
        '''
        current_time = start_time  # Creating another datetime object to keep track of time
        list_of_satellites = []  # List containing another list of satellites
        # While the tracking time is still under the starting time + duration
        while current_time <= start_time + timedelta(minutes=duration):
            # Get the visible satellite at the current time
            current_available_satellites = self.get_visibility(satlist_url=satlist_url, time=current_time,
                                                               seen_sat=seen_sats, location=location, cumulative=True)
            # Append the list into another list
            list_of_satellites.append(current_available_satellites)
            # Add the value of current_time by z (the length of the subinterval)
            current_time += timedelta(minutes=sample_interval)
        # Getting the value of the highest number of unique satellites visible and the index
        max = 0
        index = 0
        for i in range(len(list_of_satellites)):
            if len(list_of_satellites[i]) > max:
                max = len(list_of_satellites[i])
                index = i
        # Calculate the time when the num of satellite is at peak
        total_interval = sample_interval * index
        the_time = start_time + timedelta(minutes=total_interval)
        return (list_of_satellites[index], the_time)

    def getIntervalWithHighestMaximum(self, satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
    start_time=datetime.now(), n_windows=24, duration=60, sample_interval=1, location=(-37.910496, 145.134021)):
        '''
        This functions find the maximum number of satellites over multiple windows of intervals
        :param satlist_url: the url to get the list of satellites
        :param start_time: the starting time
        :param n_windows: the number of windows / how many times the duration is repeated
        :param duration: a numerical value in minutes
        :param sample_interval: the interval / tick
        :param location: the user location
        :return: a tuple containing the list of satellite and the time
        '''
        # Creating empty lists to store values
        sat_list = []
        time_list = []
        for i in range(n_windows):
            # Getting the max number of satellites on the current window
            curr_max = self.getMaxNumOfSatellitesVisible(start_time=start_time, satlist_url=satlist_url,
                                                         duration=duration, location=location,
                                                         sample_interval=sample_interval)
            # Append the result into the list
            sat_list.append(curr_max[0])
            time_list.append(curr_max[1])
            # Adding time into the start time allows the time to iterate through the windows
            start_time = start_time + timedelta(minutes=duration)
        # Getting the value of the maximum number of satellites visible and the index
        max = 0
        index = 0
        for i in range(len(time_list)):
            if len(sat_list[i]) > max:
                max = len(sat_list[i])
                index = i

        max_sat_of_all_time = sat_list[index]
        max_from_all_time = time_list[index]

        retVal = (max_sat_of_all_time, max_from_all_time)
        return retVal

    def getIntervalWithHighestTotal(self, satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
    start_time=datetime.now(), n_windows=24, duration=60, sample_interval=1, location=(-37.910496, 145.134021)):
        '''
        This function finds the highest number of unique satellites over multiple windows of duration
        :param satlist_url: the url to get the list of satellites
        :param start_time: the starting time
        :param n_windows: the number of windows / how many times the duration is repeated
        :param duration: a numerical value in minutes
        :param sample_interval: the interval / tick
        :param location: the user location
        :return: a tuple containing the list of satellite and the time
        '''
        # Creating empty lists to store values
        sat_list = []
        time_list = []
        for i in range(n_windows):
            seen_sats = []  # this list will check if the satellite is unique or not

            # Getting the highest number of unique satellites on the current window
            curr_total = self.getTotalNumOfSatellitesVisible(start_time=start_time, satlist_url=satlist_url,
                                                             duration=duration, location=location,
                                                             sample_interval=sample_interval, seen_sats=seen_sats)
            # Append the current result
            sat_list.append(curr_total[0])
            time_list.append(curr_total[1])
            # Adding time into the start time allows the time to iterate through the windows
            start_time = start_time + timedelta(minutes=duration)
        # Getting the value of the maximum number of satellites visible and the index
        max = 0
        index = 0
        for i in range(len(time_list)):
            if len(sat_list[i]) > max:
                max = len(sat_list[i])
                index = i

        total_sat_of_all_time = sat_list[index]
        total_from_all_time = time_list[index]

        retVal = (total_sat_of_all_time, total_from_all_time)
        return retVal
