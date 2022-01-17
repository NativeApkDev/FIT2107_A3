'''code to exercise the Scheduler class for FIT2107 Assignment 3'''

#from pytz import timezone
from datetime import datetime, timedelta

from scheduler import Scheduler


if __name__=="__main__":
    sched=Scheduler()
    print("Cumulative = True")
    (time, satellites) = sched.find_time(start_time=datetime.utcnow(), n_windows=5, sample_interval=5, cumulative=True)
    print(time)
    for satellite in satellites:
        print(satellite)

    print("Cumulative = False")
    (time, satellites) = sched.find_time(start_time=datetime.utcnow(), n_windows=5, sample_interval=5, cumulative=False)
    print(time)
    for satellite in satellites:
        print(satellite)

