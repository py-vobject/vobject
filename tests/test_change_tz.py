import datetime

import dateutil

from vobject.change_tz import change_tz


class StubCal:
    class StubEvent:
        class Node:
            def __init__(self, value):
                self.value = value

        def __init__(self, dtstart, dtend):
            self.dtstart = self.Node(dtstart)
            self.dtend = self.Node(dtend)

    def __init__(self, dates):
        """
        dates is a list of tuples (dtstart, dtend)
        """
        self.vevent_list = [self.StubEvent(*d) for d in dates]


def test_change_tz():
    """
    Change the timezones of events in a component to a different
    timezone
    """

    # Setup - create a stub vevent list
    old_tz = dateutil.tz.gettz("UTC")  # 0:00
    new_tz = dateutil.tz.gettz("America/Chicago")  # -5:00

    dates = [
        (
            datetime.datetime(1999, 12, 31, 23, 59, 59, 0, tzinfo=old_tz),
            datetime.datetime(2000, 1, 1, 0, 0, 0, 0, tzinfo=old_tz),
        ),
        (
            datetime.datetime(2010, 12, 31, 23, 59, 59, 0, tzinfo=old_tz),
            datetime.datetime(2011, 1, 2, 3, 0, 0, 0, tzinfo=old_tz),
        ),
    ]

    cal = StubCal(dates)

    # Exercise - change the timezone
    change_tz(cal, new_tz, dateutil.tz.gettz("UTC"))

    # Test - that the tzs were converted correctly
    expected_new_dates = [
        (
            datetime.datetime(1999, 12, 31, 17, 59, 59, 0, tzinfo=new_tz),
            datetime.datetime(1999, 12, 31, 18, 0, 0, 0, tzinfo=new_tz),
        ),
        (
            datetime.datetime(2010, 12, 31, 17, 59, 59, 0, tzinfo=new_tz),
            datetime.datetime(2011, 1, 1, 21, 0, 0, 0, tzinfo=new_tz),
        ),
    ]

    for vevent, expected_datepair in zip(cal.vevent_list, expected_new_dates):
        assert vevent.dtstart.value == expected_datepair[0]
        assert vevent.dtend.value == expected_datepair[1]


def test_change_tz_utc_only():
    """
    Change any UTC timezones of events in a component to a different
    timezone
    """

    # Setup - create a stub vevent list
    utc_tz = dateutil.tz.gettz("UTC")  # 0:00
    non_utc_tz = dateutil.tz.gettz("America/Santiago")  # -4:00
    new_tz = dateutil.tz.gettz("America/Chicago")  # -5:00

    dates = [
        (
            datetime.datetime(1999, 12, 31, 23, 59, 59, 0, tzinfo=utc_tz),
            datetime.datetime(2000, 1, 1, 0, 0, 0, 0, tzinfo=non_utc_tz),
        )
    ]

    cal = StubCal(dates)

    # Exercise - change the timezone passing utc_only=True
    change_tz(cal, new_tz, dateutil.tz.gettz("UTC"), utc_only=True)

    # Test - that only the utc item has changed
    expected_new_dates = [(datetime.datetime(1999, 12, 31, 17, 59, 59, 0, tzinfo=new_tz), dates[0][1])]

    for vevent, expected_datepair in zip(cal.vevent_list, expected_new_dates):
        assert vevent.dtstart.value == expected_datepair[0]
        assert vevent.dtend.value == expected_datepair[1]


def test_change_tz_default():
    """
    Change the timezones of events in a component to a different
    timezone, passing a default timezone that is assumed when the events
    don't have one
    """

    # Setup - create a stub vevent list
    new_tz = dateutil.tz.gettz("America/Chicago")  # -5:00

    dates = [
        (
            datetime.datetime(1999, 12, 31, 23, 59, 59, 0, tzinfo=None),
            datetime.datetime(2000, 1, 1, 0, 0, 0, 0, tzinfo=None),
        )
    ]

    cal = StubCal(dates)

    # Exercise - change the timezone
    change_tz(cal, new_tz, dateutil.tz.gettz("UTC"))

    # Test - that the tzs were converted correctly
    expected_new_dates = [
        (
            datetime.datetime(1999, 12, 31, 17, 59, 59, 0, tzinfo=new_tz),
            datetime.datetime(1999, 12, 31, 18, 0, 0, 0, tzinfo=new_tz),
        )
    ]

    for vevent, expected_datepair in zip(cal.vevent_list, expected_new_dates):
        assert vevent.dtstart.value == expected_datepair[0]
        assert vevent.dtend.value == expected_datepair[1]
