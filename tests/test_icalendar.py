import datetime
import io
import re

import dateutil
import pytest

import vobject

# Only available from CPython 3.9 onwards
try:
    import zoneinfo
except ImportError:
    pass


timezones = (
    "BEGIN:VTIMEZONE\r\n"
    "TZID:US/Pacific\r\n"
    "BEGIN:STANDARD\r\n"
    "DTSTART:19671029T020000\r\n"
    "RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=10\r\n"
    "TZOFFSETFROM:-0700\r\n"
    "TZOFFSETTO:-0800\r\n"
    "TZNAME:PST\r\n"
    "END:STANDARD\r\n"
    "BEGIN:DAYLIGHT\r\n"
    "DTSTART:19870405T020000\r\n"
    "RRULE:FREQ=YEARLY;BYDAY=1SU;BYMONTH=4\r\n"
    "TZOFFSETFROM:-0800\r\n"
    "TZOFFSETTO:-0700\r\n"
    "TZNAME:PDT\r\n"
    "END:DAYLIGHT\r\n"
    "END:VTIMEZONE\r\n"
    "\r\n"
    "BEGIN:VTIMEZONE\r\n"
    "TZID:US/Eastern\r\n"
    "BEGIN:STANDARD\r\n"
    "DTSTART:19671029T020000\r\n"
    "RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=10\r\n"
    "TZOFFSETFROM:-0400\r\n"
    "TZOFFSETTO:-0500\r\n"
    "TZNAME:EST\r\n"
    "END:STANDARD\r\n"
    "BEGIN:DAYLIGHT\r\n"
    "DTSTART:19870405T020000\r\n"
    "RRULE:FREQ=YEARLY;BYDAY=1SU;BYMONTH=4\r\n"
    "TZOFFSETFROM:-0500\r\n"
    "TZOFFSETTO:-0400\r\n"
    "TZNAME:EDT\r\n"
    "END:DAYLIGHT\r\n"
    "END:VTIMEZONE\r\n"
    "\r\n"
    "BEGIN:VTIMEZONE\r\n"
    "TZID:Santiago\r\n"
    "BEGIN:STANDARD\r\n"
    "DTSTART:19700314T000000\r\n"
    "TZOFFSETFROM:-0300\r\n"
    "TZOFFSETTO:-0400\r\n"
    "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SA\r\n"
    "TZNAME:Pacific SA Standard Time\r\n"
    "END:STANDARD\r\n"
    "BEGIN:DAYLIGHT\r\n"
    "DTSTART:19701010T000000\r\n"
    "TZOFFSETFROM:-0400\r\n"
    "TZOFFSETTO:-0300\r\n"
    "RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=2SA\r\n"
    "TZNAME:Pacific SA Daylight Time\r\n"
    "END:DAYLIGHT\r\n"
    "END:VTIMEZONE\r\n"
    "\r\n"
    "BEGIN:VTIMEZONE\r\n"
    "TZID:W. Europe\r\n"
    "BEGIN:STANDARD\r\n"
    "DTSTART:19701025T030000\r\n"
    "TZOFFSETFROM:+0200\r\n"
    "TZOFFSETTO:+0100\r\n"
    "RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU\r\n"
    "TZNAME:W. Europe Standard Time\r\n"
    "END:STANDARD\r\n"
    "BEGIN:DAYLIGHT\r\n"
    "DTSTART:19700329T020000\r\n"
    "TZOFFSETFROM:+0100\r\n"
    "TZOFFSETTO:+0200\r\n"
    "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU\r\n"
    "TZNAME:W. Europe Daylight Time\r\n"
    "END:DAYLIGHT\r\n"
    "END:VTIMEZONE\r\n"
    "\r\n"
    "BEGIN:VTIMEZONE\r\n"
    "TZID:US/Fictitious-Eastern\r\n"
    "LAST-MODIFIED:19870101T000000Z\r\n"
    "BEGIN:STANDARD\r\n"
    "DTSTART:19671029T020000\r\n"
    "RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=10\r\n"
    "TZOFFSETFROM:-0400\r\n"
    "TZOFFSETTO:-0500\r\n"
    "TZNAME:EST\r\n"
    "END:STANDARD\r\n"
    "BEGIN:DAYLIGHT\r\n"
    "DTSTART:19870405T020000\r\n"
    "RRULE:FREQ=YEARLY;BYDAY=1SU;BYMONTH=4;UNTIL=20050403T070000Z\r\n"
    "TZOFFSETFROM:-0500\r\n"
    "TZOFFSETTO:-0400\r\n"
    "TZNAME:EDT\r\n"
    "END:DAYLIGHT\r\n"
    "END:VTIMEZONE\r\n"
    "\r\n"
    "BEGIN:VTIMEZONE\r\n"
    "TZID:America/Montreal\r\n"
    "LAST-MODIFIED:20051013T233643Z\r\n"
    "BEGIN:DAYLIGHT\r\n"
    "DTSTART:20050403T070000\r\n"
    "TZOFFSETTO:-0400\r\n"
    "TZOFFSETFROM:+0000\r\n"
    "TZNAME:EDT\r\n"
    "END:DAYLIGHT\r\n"
    "BEGIN:STANDARD\r\n"
    "DTSTART:20051030T020000\r\n"
    "TZOFFSETTO:-0500\r\n"
    "TZOFFSETFROM:-0400\r\n"
    "TZNAME:EST\r\n"
    "END:STANDARD\r\n"
    "END:VTIMEZONE\r\n"
)

us_eastern = (
    "BEGIN:VTIMEZONE\r\n"
    "TZID:US/Eastern\r\n"
    "BEGIN:STANDARD\r\n"
    "DTSTART:20001029T020000\r\n"
    "RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=10;UNTIL=20061029T060000Z\r\n"
    "TZNAME:EST\r\n"
    "TZOFFSETFROM:-0400\r\n"
    "TZOFFSETTO:-0500\r\n"
    "END:STANDARD\r\n"
    "BEGIN:STANDARD\r\n"
    "DTSTART:20071104T020000\r\n"
    "RRULE:FREQ=YEARLY;BYDAY=1SU;BYMONTH=11\r\n"
    "TZNAME:EST\r\n"
    "TZOFFSETFROM:-0400\r\n"
    "TZOFFSETTO:-0500\r\n"
    "END:STANDARD\r\n"
    "BEGIN:DAYLIGHT\r\n"
    "DTSTART:20000402T020000\r\n"
    "RRULE:FREQ=YEARLY;BYDAY=1SU;BYMONTH=4;UNTIL=20060402T070000Z\r\n"
    "TZNAME:EDT\r\n"
    "TZOFFSETFROM:-0500\r\n"
    "TZOFFSETTO:-0400\r\n"
    "END:DAYLIGHT\r\n"
    "BEGIN:DAYLIGHT\r\n"
    "DTSTART:20070311T020000\r\n"
    "RRULE:FREQ=YEARLY;BYDAY=2SU;BYMONTH=3\r\n"
    "TZNAME:EDT\r\n"
    "TZOFFSETFROM:-0500\r\n"
    "TZOFFSETTO:-0400\r\n"
    "END:DAYLIGHT\r\n"
    "END:VTIMEZONE\r\n"
)

availability = (
    "BEGIN:VAVAILABILITY\r\n"
    "UID:test\r\n"
    "DTSTART:20060216T000000Z\r\n"
    "DTEND:20060217T000000Z\r\n"
    "BEGIN:AVAILABLE\r\n"
    "UID:test1\r\n"
    "DTSTART:20060216T090000Z\r\n"
    "DTEND:20060216T120000Z\r\n"
    "DTSTAMP:20060215T000000Z\r\n"
    "SUMMARY:Available in the morning\r\n"
    "END:AVAILABLE\r\n"
    "BUSYTYPE:BUSY\r\n"
    "DTSTAMP:20060215T000000Z\r\n"
    "END:VAVAILABILITY\r\n"
)

freebusy = (
    "BEGIN:VFREEBUSY\r\n"
    "UID:test\r\n"
    "DTSTART:20060216T010000Z\r\n"
    "DTEND:20060216T030000Z\r\n"
    "DTSTAMP:20060215T000000Z\r\n"
    "FREEBUSY:20060216T010000Z/PT1H\r\n"
    "FREEBUSY:20060216T010000Z/20060216T030000Z\r\n"
    "END:VFREEBUSY\r\n"
)

recurrence = (
    "BEGIN:VCALENDAR\r\n"
    "VERSION\r\n"
    " :2.0\r\n"
    "PRODID\r\n"
    " :-//Mozilla.org/NONSGML Mozilla Calendar V1.0//EN\r\n"
    "BEGIN:VEVENT\r\n"
    "CREATED\r\n"
    " :20060327T214227Z\r\n"
    "LAST-MODIFIED\r\n"
    " :20060313T080829Z\r\n"
    "DTSTAMP\r\n"
    " :20060116T231602Z\r\n"
    "UID\r\n"
    " :70922B3051D34A9E852570EC00022388\r\n"
    "SUMMARY\r\n"
    " :Monthly - All Hands Meeting with Joe Smith\r\n"
    "STATUS\r\n"
    " :CONFIRMED\r\n"
    "CLASS\r\n"
    " :PUBLIC\r\n"
    "RRULE\r\n"
    " :FREQ=MONTHLY;UNTIL=20061228;INTERVAL=1;BYDAY=4TH\r\n"
    "DTSTART\r\n"
    " :20060126T230000Z\r\n"
    "DTEND\r\n"
    " :20060127T000000Z\r\n"
    "DESCRIPTION\r\n"
    " :Repeat Meeting: - Occurs every 4th Thursday of each month\r\n"
    "END:VEVENT\r\n"
    "END:VCALENDAR\r\n"
)

recurrence_without_tz = (
    "BEGIN:VCALENDAR\r\n"
    "VERSION:2.0\r\n"
    "BEGIN:VEVENT\r\n"
    "DTSTART;VALUE=DATE:20130117\r\n"
    "DTEND;VALUE=DATE:20130118\r\n"
    "RRULE:FREQ=WEEKLY;UNTIL=20130330;BYDAY=TH\r\n"
    "SUMMARY:Meeting\r\n"
    "END:VEVENT\r\n"
    "END:VCALENDAR\r\n"
)

recurrence_offset_naive = (
    "BEGIN:VCALENDAR\r\n"
    "VERSION:2.0\r\n"
    "BEGIN:VEVENT\r\n"
    "DTSTART;VALUE=DATE:20130117\r\n"
    "DTEND;VALUE=DATE:20130118\r\n"
    "RRULE:FREQ=WEEKLY;UNTIL=20130330T230000Z;BYDAY=TH\r\n"
    "SUMMARY:Meeting\r\n"
    "END:VEVENT\r\n"
    "END:VCALENDAR\r\n"
)

vobject_0050 = (
    "BEGIN:VCALENDAR\r\n"
    "PRODID:-//Force.com Labs//iCalendar Export//EN\r\n"
    "VERSION:2.0\r\n"
    "METHOD: REQUEST\r\n"
    "CALSCALE:GREGORIAN\r\n"
    "BEGIN:VEVENT\r\n"
    "STATUS:CONFIRMED\r\n"
    "ORGANIZER;CN=Wells Fargo and Company:mailto:appointments@wellsfargo.com\r\n"
    "UID:appointments@wellsfargo.com\r\n"
    "LOCATION:POJOAQUE\r\n"
    "CREATED:20240812T192015Z\r\n"
    "DTSTART:20240812T213000Z\r\n"
    "DTEND: 20240812T223000Z\r\n"
    "TRANSP:OPAQUE\r\n"
    "DURATION:PT60M\r\n"
    "SUMMARY:Personal: Open a new account\r\n"
    "DTSTAMP:20240812T192015Z\r\n"
    "LAST-MODIFIED:20240812T192015Z\r\n"
    "SEQUENCE:0\r\n"
    "DESCRIPTION:Personal: Open a new account\r\n"
    "END:VEVENT\r\n"
    "END:VCALENDAR\r\n"
)


def test_parse_dtstart():
    """
    Should take a content line and return a datetime object.
    """
    assert vobject.icalendar.parseDtstart(
        vobject.base.textLineToContentLine("DTSTART:20060509T000000")
    ) == datetime.datetime(2006, 5, 9, 0, 0)


def test_regexes():
    """
    Test regex patterns
    """
    assert re.findall(vobject.base.P_NAME, "12foo-bar:yay") == ["12foo-bar", "yay"]
    assert re.findall(vobject.base.P_SAFE_CHAR, 'a;b"*,cd') == ["a", "b", "*", "c", "d"]
    assert re.findall(vobject.base.P_QSAFE_CHAR, 'a;b"*,cd') == ["a", ";", "b", "*", ",", "c", "d"]
    assert re.findall(
        vobject.base.P_PARAM_VALUE, '"quoted";not-quoted;start"after-illegal-quote', re.VERBOSE  # black hack
    ) == ['"quoted"', "", "not-quoted", "", "start", "", "after-illegal-quote", ""]

    match = vobject.base.line_re.match('TEST;ALTREP="http://www.wiz.org":value:;"')
    assert match.group("value") == 'value:;"'
    assert match.group("name") == "TEST"
    assert match.group("params") == ';ALTREP="http://www.wiz.org"'


def test_string_to_text_values():
    """
    Test string lists
    """
    assert vobject.icalendar.stringToTextValues("") == [""]
    assert vobject.icalendar.stringToTextValues("abcd,efgh") == ["abcd", "efgh"]


def test_string_to_period():
    """
    Test datetime strings
    """
    assert vobject.icalendar.stringToPeriod("19970101T180000Z/19970102T070000Z") == (
        datetime.datetime(1997, 1, 1, 18, 0, tzinfo=datetime.timezone.utc),
        datetime.datetime(1997, 1, 2, 7, 0, tzinfo=datetime.timezone.utc),
    )
    assert vobject.icalendar.stringToPeriod("19970101T180000Z/PT1H") == (
        datetime.datetime(1997, 1, 1, 18, 0, tzinfo=datetime.timezone.utc),
        datetime.timedelta(0, 3600),
    )


def test_timedelta_to_string():
    """
    Test timedelta strings
    """
    assert vobject.icalendar.timedeltaToString(datetime.timedelta(hours=2)) == "PT2H"
    assert vobject.icalendar.timedeltaToString(datetime.timedelta(minutes=20)) == "PT20M"


def test_delta_to_offset():
    """Test deltaToOffset() function."""

    # Sydney
    delta = datetime.timedelta(hours=10)
    assert vobject.icalendar.deltaToOffset(delta) == "+1000"

    # New York
    delta = datetime.timedelta(hours=-5)
    assert vobject.icalendar.deltaToOffset(delta), "-0500"

    # Adelaide (see https://github.com/py-vobject/vobject/pull/12)
    delta = datetime.timedelta(hours=9, minutes=30)
    assert vobject.icalendar.deltaToOffset(delta), "+0930"


def test_vtimezone_creation():
    """
    Test timezones
    """
    tzs = dateutil.tz.tzical(io.StringIO(timezones))
    pacific = vobject.icalendar.TimezoneComponent(tzs.get("US/Pacific"))
    assert str(pacific) == "<VTIMEZONE | <TZID{}US/Pacific>>"

    santiago = vobject.icalendar.TimezoneComponent(tzs.get("Santiago"))
    assert str(santiago) == "<VTIMEZONE | <TZID{}Santiago>>"

    for year in range(2001, 2010):
        for month in (2, 9):
            dt = datetime.datetime(year, month, 15, tzinfo=tzs.get("Santiago"))
            assert dt.replace(tzinfo=tzs.get("Santiago")) == dt


def test_timezone_serializing():
    """
    Serializing with timezones test
    """
    tzs = dateutil.tz.tzical(io.StringIO(timezones))
    pacific = tzs.get("US/Pacific")
    cal = vobject.base.Component("VCALENDAR")
    cal.setBehavior(vobject.icalendar.VCalendar2_0)
    ev = cal.add("vevent")
    ev.add("dtstart").value = datetime.datetime(2005, 10, 12, 9, tzinfo=pacific)

    evruleset = dateutil.rrule.rruleset()
    evruleset.rrule(
        dateutil.rrule.rrule(
            dateutil.rrule.WEEKLY, interval=2, byweekday=[2, 4], until=datetime.datetime(2005, 12, 15, 9)
        )
    )
    evruleset.rrule(dateutil.rrule.rrule(dateutil.rrule.MONTHLY, bymonthday=[-1, -5]))
    evruleset.exdate(datetime.datetime(2005, 10, 14, 9, tzinfo=pacific))
    ev.rruleset = evruleset
    ev.add("duration").value = datetime.timedelta(hours=1)

    apple = tzs.get("America/Montreal")
    ev.dtstart.value = datetime.datetime(2005, 10, 12, 9, tzinfo=apple)


def test_pytz_timezone_serializing():
    """
    Serializing with timezones from pytz test
    """
    try:
        import pytz
    except ImportError:
        pytest.skip("pytz not installed")

    # Avoid conflicting cached tzinfo from other tests
    def unregister_tzid(tzid):
        """Clear tzid from icalendar TZID registry"""
        if vobject.icalendar.getTzid(tzid, False):
            vobject.icalendar.registerTzid(tzid, None)

    unregister_tzid("US/Eastern")
    eastern = pytz.timezone("US/Eastern")
    cal = vobject.base.Component("VCALENDAR")
    cal.setBehavior(vobject.icalendar.VCalendar2_0)
    ev = cal.add("vevent")
    ev.add("dtstart").value = eastern.localize(datetime.datetime(2008, 10, 12, 9))
    serialized = cal.serialize()

    assert us_eastern.replace("\r\n", "\n") in serialized.replace("\r\n", "\n")

    # Exhaustively test all zones (just looking for no errors)
    for tzname in pytz.all_timezones:
        unregister_tzid(tzname)
        tz = vobject.icalendar.TimezoneComponent(tzinfo=pytz.timezone(tzname))
        tz.serialize()


def test_free_busy():
    """
    Test freebusy components
    """
    vfb = vobject.base.newFromBehavior("VFREEBUSY")
    vfb.add("uid").value = "test"
    vfb.add("dtstamp").value = datetime.datetime(2006, 2, 15, 0, tzinfo=dateutil.tz.tzutc())
    vfb.add("dtstart").value = datetime.datetime(2006, 2, 16, 1, tzinfo=dateutil.tz.tzutc())
    vfb.add("dtend").value = vfb.dtstart.value + datetime.timedelta(hours=2)
    vfb.add("freebusy").value = [(vfb.dtstart.value, datetime.timedelta(hours=1))]
    vfb.add("freebusy").value = [(vfb.dtstart.value, vfb.dtend.value)]

    assert vfb.serialize().replace("\r\n", "\n") == freebusy.replace("\r\n", "\n")


def test_availability():
    """
    Test availability components
    """
    vcal = vobject.base.newFromBehavior("VAVAILABILITY")
    vcal.add("uid").value = "test"
    vcal.add("dtstamp").value = datetime.datetime(2006, 2, 15, 0, tzinfo=dateutil.tz.tzutc())
    vcal.add("dtstart").value = datetime.datetime(2006, 2, 16, 0, tzinfo=dateutil.tz.tzutc())
    vcal.add("dtend").value = datetime.datetime(2006, 2, 17, 0, tzinfo=dateutil.tz.tzutc())
    vcal.add("busytype").value = "BUSY"

    av = vobject.base.newFromBehavior("AVAILABLE")
    av.add("uid").value = "test1"
    av.add("dtstamp").value = datetime.datetime(2006, 2, 15, 0, tzinfo=dateutil.tz.tzutc())
    av.add("dtstart").value = datetime.datetime(2006, 2, 16, 9, tzinfo=dateutil.tz.tzutc())
    av.add("dtend").value = datetime.datetime(2006, 2, 16, 12, tzinfo=dateutil.tz.tzutc())
    av.add("summary").value = "Available in the morning"
    vcal.add(av)

    assert vcal.serialize().replace("\r\n", "\n") == availability.replace("\r\n", "\n")


def test_recurrence():
    """
    Ensure date valued UNTILs in rrules are in a reasonable timezone,
    and include that day (12/28 in this test)
    """
    cal = vobject.base.readOne(recurrence)
    dates = list(cal.vevent.getrruleset())
    assert dates[0] == datetime.datetime(2006, 1, 26, 23, 0, tzinfo=dateutil.tz.tzutc())
    assert dates[1] == datetime.datetime(2006, 2, 23, 23, 0, tzinfo=dateutil.tz.tzutc())
    assert dates[-1] == datetime.datetime(2006, 12, 28, 23, 0, tzinfo=dateutil.tz.tzutc())


def test_recurring_component():
    """
    Test recurring events
    """
    # init
    vevent = vobject.icalendar.RecurringComponent(name="VEVENT")
    assert vevent.isNative

    # rruleset should be None at this point.
    # No rules have been passed or created.
    assert vevent.rruleset is None

    # Now add start and rule for recurring event
    vevent.add("dtstart").value = datetime.datetime(2005, 1, 19, 9)
    vevent.add("rrule").value = "FREQ=WEEKLY;COUNT=2;INTERVAL=2;BYDAY=TU,TH"
    assert list(vevent.rruleset) == [datetime.datetime(2005, 1, 20, 9, 0), datetime.datetime(2005, 2, 1, 9, 0)]
    assert list(vevent.getrruleset(addRDate=True)) == [
        datetime.datetime(2005, 1, 19, 9, 0),
        datetime.datetime(2005, 1, 20, 9, 0),
    ]

    # Also note that dateutil will expand all-day events (datetime.date values)
    # to datetime.datetime value with time 0 and no timezone.
    vevent.dtstart.value = datetime.date(2005, 3, 18)
    assert list(vevent.rruleset) == [datetime.datetime(2005, 3, 29, 0, 0), datetime.datetime(2005, 3, 31, 0, 0)]
    assert list(vevent.getrruleset(True)) == [
        datetime.datetime(2005, 3, 18, 0, 0),
        datetime.datetime(2005, 3, 29, 0, 0),
    ]


def test_recurrence_without_tz():
    """
    Test recurring vevent missing any time zone definitions.
    """

    cal = vobject.base.readOne(recurrence_without_tz)
    dates = list(cal.vevent.getrruleset())
    assert dates[0] == datetime.datetime(2013, 1, 17, 0, 0)
    assert dates[1] == datetime.datetime(2013, 1, 24, 0, 0)
    assert dates[-1] == datetime.datetime(2013, 3, 28, 0, 0)


def test_recurrence_offset_naive():
    """
    Ensure recurring vevent missing some time zone definitions is
    parsing. See issue #75.
    """
    cal = vobject.base.readOne(recurrence_offset_naive)
    dates = list(cal.vevent.getrruleset())
    assert dates[0] == datetime.datetime(2013, 1, 17, 0, 0)
    assert dates[1] == datetime.datetime(2013, 1, 24, 0, 0)
    assert dates[-1] == datetime.datetime(2013, 3, 28, 0, 0)


def test_issue50():
    """
    Ensure leading spaces in a DATE-TIME value are ignored when not in
    strict mode.

    See https://github.com/py-vobject/vobject/issues/50
    """
    cal = vobject.base.readOne(vobject_0050)
    assert cal.vevent.dtend.value == datetime.datetime(2024, 8, 12, 22, 30, tzinfo=dateutil.tz.tzutc())


def test_includes_dst_offset():
    tz = dateutil.tz.gettz("US/Eastern")
    assert tz is not None

    # Simple first
    dt = datetime.datetime(2020, 1, 1)
    assert not vobject.icalendar.includes_dst_offset(tz, dt)
    dt = datetime.datetime(2020, 7, 1)
    assert vobject.icalendar.includes_dst_offset(tz, dt)

    # Leaving DST: 2024-11-03 02:00:00 reverts to 01:00


def test_omits_dst_offset():

    # Check dateutil, pytz, and zoneinfo (3.9+) tzinfo instances
    _timezones = []
    if "dateutil" in globals():
        tz = dateutil.tz.gettz("America/New_York")
        assert tz is not None
        _timezones.append(tz)
    if "zoneinfo" in globals():
        tz = zoneinfo.ZoneInfo("America/New_York")
        assert tz is not None
        _timezones.append(tz)

    for tz in _timezones:
        dt = datetime.datetime(2020, 1, 1)
        assert vobject.icalendar.omits_dst_offset(tz, dt)

        dt = datetime.datetime(2020, 7, 1)
        assert not vobject.icalendar.omits_dst_offset(tz, dt)

        # Entering DST: 2024-03-10 02:00:00 advances to 03:00
        dt = datetime.datetime(2024, 3, 10, 1, 59, 59)
        assert vobject.icalendar.omits_dst_offset(tz, dt)

        dt = datetime.datetime(2024, 3, 10, 3, 0, 0)
        assert not vobject.icalendar.omits_dst_offset(tz, dt)

        dt = datetime.datetime(2024, 3, 10, 3, 0, 1)
        assert not vobject.icalendar.omits_dst_offset(tz, dt)

        # Leaving DST: 2024-11-03 02:00:00 reverts to 01:00:00
        dt = datetime.datetime(2024, 11, 3, 1, 0, 0)  # fold=0
        assert not vobject.icalendar.omits_dst_offset(tz, dt)

        dt = datetime.datetime(2024, 11, 3, 1, 59, 59)  # fold=0
        assert not vobject.icalendar.omits_dst_offset(tz, dt)

        dt = datetime.datetime(2024, 11, 3, 1, 0, 0, fold=1)
        assert vobject.icalendar.omits_dst_offset(tz, dt)

        dt = datetime.datetime(2024, 11, 3, 2, 0, 0, fold=1)
        assert vobject.icalendar.omits_dst_offset(tz, dt)

        dt = datetime.datetime(2024, 11, 3, 2, 0, 1, fold=0)
        assert vobject.icalendar.omits_dst_offset(tz, dt)


def test_first_transition_all_match():
    dts = [
        datetime.datetime(2000, 1, 1, 0, 0, 0),
        datetime.datetime(2000, 1, 1, 1, 0, 0),
        datetime.datetime(2000, 1, 1, 2, 0, 0),
        datetime.datetime(2000, 1, 1, 3, 0, 0),
    ]

    # All datetimes have seconds value of zero, so match, so expecting 'None'
    result = vobject.icalendar.first_transition(dateutil.tz.tzutc(), dts, lambda tz, dt: dt.second == 0)
    assert result is None


def test_first_transition_none_match():
    dts = [
        datetime.datetime(2000, 1, 1, 0, 0, 1),
        datetime.datetime(2000, 1, 1, 1, 0, 1),
        datetime.datetime(2000, 1, 1, 2, 0, 1),
        datetime.datetime(2000, 1, 1, 3, 0, 1),
    ]

    # No datetimes have seconds value of zero, so none match, so first? or last? match FIXME!
    result = vobject.icalendar.first_transition(dateutil.tz.tzutc(), dts, lambda tz, dt: dt.second == 0)
    assert result == dts[3]


def test_first_transition_last_not_match():
    dts = [
        datetime.datetime(2000, 1, 1, 0, 0, 0),
        datetime.datetime(2000, 1, 1, 1, 0, 0),
        datetime.datetime(2000, 1, 1, 2, 0, 0),
        datetime.datetime(2000, 1, 1, 3, 0, 1),
    ]

    result = vobject.icalendar.first_transition(dateutil.tz.tzutc(), dts, lambda tz, dt: dt.second == 0)
    assert result == dts[3]


def test_first_transition_first_not_match():
    dts = [
        datetime.datetime(2000, 1, 1, 0, 0, 1),
        datetime.datetime(2000, 1, 1, 1, 0, 0),
        datetime.datetime(2000, 1, 1, 2, 0, 0),
        datetime.datetime(2000, 1, 1, 3, 0, 0),
    ]

    result = vobject.icalendar.first_transition(dateutil.tz.tzutc(), dts, lambda tz, dt: dt.second == 0)
    assert result == dts[0]


def test_first_transition_multi_not_match():
    dts = [
        datetime.datetime(2000, 1, 1, 0, 0, 0),
        datetime.datetime(2000, 1, 1, 1, 0, 1),
        datetime.datetime(2000, 1, 1, 2, 0, 0),
        datetime.datetime(2000, 1, 1, 3, 0, 1),
    ]

    result = vobject.icalendar.first_transition(dateutil.tz.tzutc(), dts, lambda tz, dt: dt.second == 0)
    assert result == dts[1]
