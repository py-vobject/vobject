import datetime
import io
import re
import zoneinfo

import dateutil
import pytest

import vobject

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
    assert str(pacific) == "<VTIMEZONE | <TZID{}[]US/Pacific>>"

    santiago = vobject.icalendar.TimezoneComponent(tzs.get("Santiago"))
    assert str(santiago) == "<VTIMEZONE | <TZID{}[]Santiago>>"

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


def _tzid_only_event(tzid, start):
    return (
        "BEGIN:VCALENDAR\r\n"
        "VERSION:2.0\r\n"
        "PRODID:test\r\n"
        "BEGIN:VEVENT\r\n"
        "UID:test\r\n"
        "DTSTAMP:20260101T000000Z\r\n"
        f"DTSTART;TZID={tzid}:{start}\r\n"
        "END:VEVENT\r\n"
        "END:VCALENDAR\r\n"
    )


def _stored_vtimezone_tzinfo(serialized):
    """
    Return the tzinfo of the serialized VTIMEZONE only.

    Reading the whole calendar back could resolve the TZID through the
    process-wide TZID registry instead of the stored VTIMEZONE.
    """
    start = serialized.index("BEGIN:VTIMEZONE")
    end = serialized.index("END:VTIMEZONE") + len("END:VTIMEZONE")
    return vobject.icalendar.TimezoneComponent.gettzinfo(vobject.readOne(serialized[start:end]))


@pytest.mark.parametrize(
    "tzid, start, offset_hours",
    [
        # before 2000: 1995 US rules, DST from April 2 to October 29
        ("America/Chicago", "19950715T120000", -5),
        # 2000-2006 rules also give -6 here; the extended range must not break it
        ("America/Chicago", "19951030T120000", -6),
        # southern hemisphere: daylight time already in effect on January 1
        ("Australia/Sydney", "19900301T120000", 11),
        ("Australia/Sydney", "19900601T120000", 10),
        # inside the default range, unchanged
        ("America/Chicago", "20260715T120000", -5),
        ("America/Chicago", "20261201T120000", -6),
        # Israel, last Friday of March: the 2027 onset ends a bounded rule
        ("Asia/Jerusalem", "20270326T120000", 3),
        # after 2030: rules are generated through the event's year
        ("Asia/Jerusalem", "20310401T120000", 3),
        # unchanged after 2030 where the last rule still holds
        ("America/Chicago", "20350715T120000", -5),
        # after 2037: the last rule stays open-ended, DST is not dropped
        ("America/Chicago", "20500715T120000", -5),
        ("America/Chicago", "20501201T120000", -6),
    ],
)
def test_generated_vtimezone_covers_event_year(tzid, start, offset_hours):
    """
    A VTIMEZONE generated for a TZID without one covers the event's year.
    """
    serialized = vobject.readOne(_tzid_only_event(tzid, start)).serialize()
    tzinfo = _stored_vtimezone_tzinfo(serialized)
    naive = datetime.datetime.strptime(start, "%Y%m%dT%H%M%S")
    assert naive.replace(tzinfo=tzinfo).utcoffset() == datetime.timedelta(hours=offset_hours)


def test_generated_vtimezone_default_range_output_unchanged():
    """
    Events inside 2001-2030 get the same VTIMEZONE as before.
    """
    serialized = vobject.readOne(_tzid_only_event("America/Chicago", "20260715T120000")).serialize()
    default = vobject.icalendar.TimezoneComponent(tzinfo=vobject.icalendar.getTzid("America/Chicago")).serialize()
    assert default in serialized


def test_vtimezone_years():
    years = vobject.icalendar.vtimezoneYears
    assert years([]) == (2000, 2030)
    assert years([2001, 2030]) == (2000, 2030)
    assert years([2000]) == (1999, 2030)
    assert years([1995, 2026]) == (1994, 2030)
    assert years([2035]) == (2000, 2035)
    assert years([2050]) == (2000, 2037)
    assert years([1]) == (1900, 2030)


def test_datetime_years():
    years = vobject.icalendar.datetimeYears
    utc = datetime.timezone.utc
    assert years(datetime.datetime(1995, 7, 15, 12)) == [1995]
    assert not years(datetime.date(1995, 7, 15))
    assert not years("19950715T120000")
    assert years([datetime.datetime(1995, 1, 1), datetime.datetime(2050, 1, 1)]) == [1995, 2050]
    assert years([(datetime.datetime(1990, 1, 1, tzinfo=utc), datetime.timedelta(hours=1))]) == [1990]


# Israel 2024-2027: DST starts on the last Friday of March at 02:00 local
# time. 2027-03-26 02:00 at +02:00 is 2027-03-26 00:00 UTC, the UNTIL below.
until_east_of_utc = (
    "BEGIN:VTIMEZONE\r\n"
    "TZID:Test/UntilEast\r\n"
    "BEGIN:STANDARD\r\n"
    "DTSTART:20231027T020000\r\n"
    "RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=10\r\n"
    "TZOFFSETFROM:+0300\r\n"
    "TZOFFSETTO:+0200\r\n"
    "END:STANDARD\r\n"
    "BEGIN:DAYLIGHT\r\n"
    "DTSTART:20240329T020000\r\n"
    "RRULE:FREQ=YEARLY;BYDAY=-1FR;BYMONTH=3;UNTIL=20270326T000000Z\r\n"
    "TZOFFSETFROM:+0200\r\n"
    "TZOFFSETTO:+0300\r\n"
    "END:DAYLIGHT\r\n"
    "END:VTIMEZONE\r\n"
)

# US 1987-2006: DST ends on the last Sunday of October at 02:00 local time.
# 2006-10-29 02:00 at -05:00 is 2006-10-29 07:00 UTC, the UNTIL below.
until_west_of_utc = (
    "BEGIN:VTIMEZONE\r\n"
    "TZID:Test/UntilWest\r\n"
    "BEGIN:STANDARD\r\n"
    "DTSTART:19871025T020000\r\n"
    "RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=10;UNTIL=20061029T070000Z\r\n"
    "TZOFFSETFROM:-0500\r\n"
    "TZOFFSETTO:-0600\r\n"
    "END:STANDARD\r\n"
    "BEGIN:DAYLIGHT\r\n"
    "DTSTART:19870405T020000\r\n"
    "RRULE:FREQ=YEARLY;BYDAY=1SU;BYMONTH=4;UNTIL=20060402T080000Z\r\n"
    "TZOFFSETFROM:-0600\r\n"
    "TZOFFSETTO:-0500\r\n"
    "END:DAYLIGHT\r\n"
    "END:VTIMEZONE\r\n"
)


@pytest.mark.parametrize(
    "vtimezone, local, offset_hours",
    [
        # the final onset, exactly at UNTIL, is kept
        (until_east_of_utc, datetime.datetime(2027, 3, 26, 12), 3),
        (until_east_of_utc, datetime.datetime(2026, 3, 27, 12), 3),
        (until_east_of_utc, datetime.datetime(2027, 3, 25, 12), 2),
        (until_west_of_utc, datetime.datetime(2006, 10, 28, 12), -5),
        (until_west_of_utc, datetime.datetime(2006, 10, 30, 12), -6),
    ],
)
def test_vtimezone_utc_until_keeps_final_onset(vtimezone, local, offset_hours):
    """
    A UTC UNTIL equal to a rule's final onset keeps that onset (RFC 5545).
    """
    tzinfo = vobject.icalendar.TimezoneComponent.gettzinfo(vobject.readOne(vtimezone))
    assert local.replace(tzinfo=tzinfo).utcoffset() == datetime.timedelta(hours=offset_hours)


@pytest.mark.parametrize(
    "rule, offsetfrom, expected",
    [
        ("FREQ=YEARLY;UNTIL=20270326T000000Z", "+0200", "FREQ=YEARLY;UNTIL=20270326T020000"),
        ("UNTIL=20270325T203000Z;FREQ=YEARLY", "+0530", "UNTIL=20270326T020000;FREQ=YEARLY"),
        ("FREQ=YEARLY;until=20270326T000000z", "+013045", "FREQ=YEARLY;until=20270326T013045"),
        # unchanged: west of UTC or zero offset, no UTC UNTIL, a DATE UNTIL,
        # a local UNTIL, a bad offset, an overflow
        ("FREQ=YEARLY;UNTIL=20061029T070000Z", "-0500", "FREQ=YEARLY;UNTIL=20061029T070000Z"),
        ("FREQ=YEARLY;UNTIL=20061029T070000Z", "+0000", "FREQ=YEARLY;UNTIL=20061029T070000Z"),
        ("FREQ=YEARLY;BYMONTH=3", "+0200", "FREQ=YEARLY;BYMONTH=3"),
        ("FREQ=YEARLY;UNTIL=20270326", "+0200", "FREQ=YEARLY;UNTIL=20270326"),
        ("FREQ=YEARLY;UNTIL=20270326T000000", "+0200", "FREQ=YEARLY;UNTIL=20270326T000000"),
        ("FREQ=YEARLY;UNTIL=20270326T000000Z", "bad", "FREQ=YEARLY;UNTIL=20270326T000000Z"),
        ("FREQ=YEARLY;UNTIL=99991231T235959Z", "+0100", "FREQ=YEARLY;UNTIL=99991231T235959Z"),
    ],
)
def test_local_until(rule, offsetfrom, expected):
    assert vobject.icalendar.localUntil(rule, offsetfrom) == expected


def test_vtimezone_rrule_parameter_is_kept():
    """
    An observance RRULE with a parameter still parses when UNTIL is rewritten.
    """
    vtimezone = until_east_of_utc.replace("RRULE:FREQ=YEARLY;BYDAY=-1FR", "RRULE;X-TEST=yes:FREQ=YEARLY;BYDAY=-1FR")
    component = vobject.readOne(vtimezone)
    tzinfo = vobject.icalendar.TimezoneComponent.gettzinfo(component)
    assert datetime.datetime(2027, 3, 26, 12, tzinfo=tzinfo).utcoffset() == datetime.timedelta(hours=3)
    assert component.daylight.rrule.params == {"X-TEST": ["yes"]}


def test_vtimezone_west_of_utc_local_until_unchanged():
    """
    West of UTC, an UNTIL written as local time with Z reads as before.
    """
    vtimezone = until_west_of_utc.replace("UNTIL=20061029T070000Z", "UNTIL=20061029T020000Z")
    tzinfo = vobject.icalendar.TimezoneComponent.gettzinfo(vobject.readOne(vtimezone))
    assert datetime.datetime(2006, 10, 30, 12, tzinfo=tzinfo).utcoffset() == datetime.timedelta(hours=-6)


@pytest.mark.parametrize(
    "tzid, start",
    [
        # before the 1900 floor
        ("America/Chicago", "00010601T120000"),
        ("Europe/Berlin", "00020601T120000"),
        # early history that breaks settzinfo's assumptions with pytz
        ("America/Bahia", "19100715T120000"),
        ("Asia/Kuala_Lumpur", "19330715T120000"),
    ],
)
def test_generated_vtimezone_early_dates_serialize(tzid, start):
    """
    Early dates still serialize, with a VTIMEZONE for the TZID.
    """
    serialized = vobject.readOne(_tzid_only_event(tzid, start)).serialize()
    assert f"TZID:{tzid}" in serialized


def test_generated_vtimezone_falls_back_to_default_range(monkeypatch):
    """
    If settzinfo fails for the extended range, the default range is used.
    """
    original = vobject.icalendar.TimezoneComponent.settzinfo

    def settzinfo(self, tzinfo, start=2000, end=2030):
        if (start, end) != (2000, 2030):
            raise OverflowError("date value out of range")
        return original(self, tzinfo, start, end)

    monkeypatch.setattr(vobject.icalendar.TimezoneComponent, "settzinfo", settzinfo)
    serialized = vobject.readOne(_tzid_only_event("America/Chicago", "19950715T120000")).serialize()
    default = vobject.icalendar.TimezoneComponent(tzinfo=vobject.icalendar.getTzid("America/Chicago")).serialize()
    assert default in serialized


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


def test_rrdate_with_period():
    """
    Test round-trip parsing and serialization of an RRULE with
    an RDATE using a PERIOD.
    """

    raw = (
        "BEGIN:VCALENDAR\r\n"
        + "VERSION:2.0\r\n"
        + "PRODID:test\r\n"
        + "BEGIN:VEVENT\r\n"
        + "UID:test\r\n"
        + "DTSTART:20000101T000000Z\r\n"
        + "DURATION:PT1H\r\n"
        + "DTSTAMP:20000101T000000Z\r\n"
        + "RDATE;VALUE=PERIOD:20000102T000000Z/PT2H\r\n"
        + "RRULE:FREQ=WEEKLY\r\n"
        + "END:VEVENT\r\n"
        + "END:VCALENDAR\r\n"
    )
    obj = vobject.readOne(raw)
    serialized = obj.serialize()
    assert raw == serialized


def test_recurrence_rdate_implicit_datetime_value():
    raw = (
        "BEGIN:VCALENDAR\r\n"
        + "VERSION:2.0\r\n"
        + "PRODID:test\r\n"
        + "BEGIN:VEVENT\r\n"
        + "UID:test\r\n"
        + "DTSTART:20000101T000000Z\r\n"
        + "DTSTAMP:20000101T000000Z\r\n"
        + "DURATION:PT1H\r\n"
        + "RDATE:20000104T090000Z\r\n"
        + "END:VEVENT\r\n"
        + "END:VCALENDAR\r\n"
    )
    cal = vobject.readOne(raw)
    rrs = cal.vevent.getrruleset()
    dates = list(rrs.xafter(dateutil.parser.parse("19700101T000000Z")))
    assert len(dates) == 1
    assert dates[0] == dateutil.parser.parse("20000104T090000Z")


def test_serialize_rdate_implicit_datetime_value():
    raw = (
        "BEGIN:VCALENDAR\r\n"
        + "VERSION:2.0\r\n"
        + "PRODID:test\r\n"
        + "BEGIN:VEVENT\r\n"
        + "UID:test\r\n"
        + "DTSTART:20000101T000000Z\r\n"
        + "DTSTAMP:20000101T000000Z\r\n"
        + "DURATION:PT1H\r\n"
        + "RDATE:20000104T090000Z\r\n"
        + "END:VEVENT\r\n"
        + "END:VCALENDAR\r\n"
    )
    cal = vobject.readOne(raw)
    serialized = cal.serialize()
    assert "RDATE:20000104T090000Z" in serialized


def test_recurrence_rdate_bad_implicit_datetime_value():
    raw = (
        "BEGIN:VCALENDAR\r\n"
        + "VERSION:2.0\r\n"
        + "PRODID:test\r\n"
        + "BEGIN:VEVENT\r\n"
        + "UID:test\r\n"
        + "DTSTART:20000101T000000Z\r\n"
        + "DTSTAMP:20000101T000000Z\r\n"
        + "DURATION:PT1H\r\n"
        + "RDATE:bogus\r\n"
        + "END:VEVENT\r\n"
        + "END:VCALENDAR\r\n"
    )
    with pytest.raises(vobject.base.ParseError):
        vobject.readOne(raw)


def test_recurrence_rate_explicit_datetime_value():
    raw = (
        "BEGIN:VCALENDAR\r\n"
        + "VERSION:2.0\r\n"
        + "PRODID:test\r\n"
        + "BEGIN:VEVENT\r\n"
        + "UID:test\r\n"
        + "DTSTART:20000101T000000Z\r\n"
        + "DTSTAMP:20000101T000000Z\r\n"
        + "DURATION:PT1H\r\n"
        + "RDATE;VALUE=DATE-TIME:20000104T090000Z\r\n"
        + "END:VEVENT\r\n"
        + "END:VCALENDAR\r\n"
    )
    cal = vobject.readOne(raw)
    rrs = cal.vevent.getrruleset()
    dates = list(rrs.xafter(dateutil.parser.parse("19700101T000000Z")))
    assert len(dates) == 1
    assert dates[0] == dateutil.parser.parse("20000104T090000Z")


def test_recurrence_rdate_bad_explicit_datetime_value():
    raw = (
        "BEGIN:VCALENDAR\r\n"
        + "VERSION:2.0\r\n"
        + "PRODID:test\r\n"
        + "BEGIN:VEVENT\r\n"
        + "UID:test\r\n"
        + "DTSTART:20000101T000000Z\r\n"
        + "DTSTAMP:20000101T000000Z\r\n"
        + "DURATION:PT1H\r\n"
        + "RDATE;VALUE=DATE-TIME:bogus\r\n"
        + "END:VEVENT\r\n"
        + "END:VCALENDAR\r\n"
    )
    with pytest.raises(vobject.base.ParseError):
        vobject.readOne(raw)


def test_recurrence_rdate_explicit_date_value():
    raw = (
        "BEGIN:VCALENDAR\r\n"
        + "VERSION:2.0\r\n"
        + "PRODID:test\r\n"
        + "BEGIN:VEVENT\r\n"
        + "UID:test\r\n"
        + "DTSTART:20000101T000000Z\r\n"
        + "DTSTAMP:20000101T000000Z\r\n"
        + "DURATION:PT1H\r\n"
        + "RDATE;VALUE=DATE:20000104\r\n"
        + "END:VEVENT\r\n"
        + "END:VCALENDAR\r\n"
    )
    cal = vobject.readOne(raw)
    rrs = cal.vevent.getrruleset()
    dates = list(rrs.xafter(dateutil.parser.parse("19700101")))
    assert len(dates) == 1
    assert dates[0] == dateutil.parser.parse("20000104")


def test_recurrence_rdate_bad_explicit_date_value():
    raw = (
        "BEGIN:VCALENDAR\r\n"
        + "VERSION:2.0\r\n"
        + "PRODID:test\r\n"
        + "BEGIN:VEVENT\r\n"
        + "UID:test\r\n"
        + "DTSTART:20000101T000000Z\r\n"
        + "DTSTAMP:20000101T000000Z\r\n"
        + "DURATION:PT1H\r\n"
        + "RDATE;VALUE=DATE:bogus\r\n"
        + "END:VEVENT\r\n"
        + "END:VCALENDAR\r\n"
    )
    with pytest.raises(vobject.base.ParseError):
        vobject.readOne(raw)


def test_recurrence_rdate_period_datetimes_value():
    raw = (
        "BEGIN:VCALENDAR\r\n"
        + "VERSION:2.0\r\n"
        + "PRODID:test\r\n"
        + "BEGIN:VEVENT\r\n"
        + "UID:test\r\n"
        + "DTSTART:20000101T000000Z\r\n"
        + "DTSTAMP:20000101T000000Z\r\n"
        + "DURATION:PT1H\r\n"
        + "RDATE;VALUE=PERIOD:20000104T090000Z/20000104T110000Z\r\n"
        + "END:VEVENT\r\n"
        + "END:VCALENDAR\r\n"
    )
    cal = vobject.readOne(raw)
    rrs = cal.vevent.getrruleset()
    dates = list(rrs.xafter(dateutil.parser.parse("19700101T000000Z")))
    assert len(dates) == 1
    assert dates[0] == dateutil.parser.parse("20000104T090000Z")


def test_recurrence_rdate_period_datetime_duration_value():
    raw = (
        "BEGIN:VCALENDAR\r\n"
        + "VERSION:2.0\r\n"
        + "PRODID:test\r\n"
        + "BEGIN:VEVENT\r\n"
        + "UID:test\r\n"
        + "DTSTART:20000101T000000Z\r\n"
        + "DTSTAMP:20000101T000000Z\r\n"
        + "DURATION:PT1H\r\n"
        + "RDATE;VALUE=PERIOD:20000104T090000Z/PT3H\r\n"
        + "END:VEVENT\r\n"
        + "END:VCALENDAR\r\n"
    )
    cal = vobject.readOne(raw)
    rrs = cal.vevent.getrruleset()
    dates = list(rrs.xafter(dateutil.parser.parse("19700101T000000Z")))
    assert len(dates) == 1
    assert dates[0] == dateutil.parser.parse("20000104T090000Z")


def test_recurrence_rdate_bad_explicit_period_value():
    raw = (
        "BEGIN:VCALENDAR\r\n"
        + "VERSION:2.0\r\n"
        + "PRODID:test\r\n"
        + "BEGIN:VEVENT\r\n"
        + "UID:test\r\n"
        + "DTSTART:20000101T000000Z\r\n"
        + "DTSTAMP:20000101T000000Z\r\n"
        + "DURATION:PT1H\r\n"
        + "RDATE;VALUE=PERIOD:bogus\r\n"
        + "END:VEVENT\r\n"
        + "END:VCALENDAR\r\n"
    )
    with pytest.raises(vobject.base.ParseError):
        vobject.readOne(raw)


# --- RDATE / EXDATE serialization and validation (MultiDateBehavior) -------

MULTIDATE_HEAD = (
    "BEGIN:VCALENDAR\r\n"
    "VERSION:2.0\r\n"
    "PRODID:test\r\n"
    "BEGIN:VEVENT\r\n"
    "UID:test\r\n"
    "DTSTART:20000101T090000Z\r\n"
    "DTSTAMP:20000101T000000Z\r\n"
)
MULTIDATE_TAIL = "END:VEVENT\r\nEND:VCALENDAR\r\n"
NEW_YORK = zoneinfo.ZoneInfo("America/New_York")
UTC = vobject.icalendar.utc
HOUR = datetime.timedelta(hours=1)


def multidate_calendar(name, value, value_param=None):
    """Return a calendar with one event that has a name property set to value."""
    cal = vobject.iCalendar()
    event = cal.add("vevent")
    event.add("uid").value = "test"
    event.add("dtstart").value = datetime.datetime(2000, 1, 1, 9, tzinfo=UTC)
    line = event.add(name)
    line.value = value
    if value_param is not None:
        line.value_param = value_param
    return cal


def property_lines(serialized, name):
    """Return the unfolded lines of serialized for property name."""
    return [line for line in serialized.replace("\r\n ", "").splitlines() if re.match(f"{name}[;:]", line)]


def test_serialize_exdate_implicit_datetime_value():
    cal = vobject.readOne(MULTIDATE_HEAD + "EXDATE:20000104T090000Z,20000105T090000Z\r\n" + MULTIDATE_TAIL)
    assert property_lines(cal.serialize(), "EXDATE") == ["EXDATE:20000104T090000Z,20000105T090000Z"]


def test_serialize_exdate_explicit_datetime_value_kept():
    cal = vobject.readOne(MULTIDATE_HEAD + "EXDATE;VALUE=DATE-TIME:20000104T090000Z\r\n" + MULTIDATE_TAIL)
    assert property_lines(cal.serialize(), "EXDATE") == ["EXDATE;VALUE=DATE-TIME:20000104T090000Z"]


def test_serialize_floating_and_utc_datetimes():
    """Floating and UTC date-times can share a line: neither needs a TZID."""
    raw = MULTIDATE_HEAD + "EXDATE:20000104T090000Z,20000105T090000\r\n" + MULTIDATE_TAIL
    cal = vobject.readOne(raw)
    assert property_lines(cal.serialize(), "EXDATE") == ["EXDATE:20000104T090000Z,20000105T090000"]


@pytest.mark.parametrize(
    "period, expected",
    [
        ((datetime.datetime(2000, 1, 4, 9, tzinfo=UTC), HOUR), "RDATE;VALUE=PERIOD:20000104T090000Z/PT1H"),
        (
            (datetime.datetime(2000, 1, 4, 9, tzinfo=UTC), datetime.datetime(2000, 1, 4, 10, tzinfo=UTC)),
            "RDATE;VALUE=PERIOD:20000104T090000Z/20000104T100000Z",
        ),
    ],
)
def test_serialize_rdate_periods_without_value_param(period, expected):
    cal = multidate_calendar("rdate", [period])
    assert property_lines(cal.serialize(), "RDATE") == [expected]


def test_serialize_parsed_exdate_with_value_replaced_by_dates():
    cal = vobject.readOne(MULTIDATE_HEAD + "EXDATE:20000104T090000Z\r\n" + MULTIDATE_TAIL)
    cal.vevent.exdate.value = [datetime.date(2000, 1, 4)]
    assert property_lines(cal.serialize(), "EXDATE") == ["EXDATE;VALUE=DATE:20000104"]


def test_serialize_stale_value_param_replaced():
    """VALUE follows the values, not a leftover parameter."""
    cal = multidate_calendar("exdate", [datetime.datetime(2000, 1, 4, 9, tzinfo=UTC)], value_param="DATE")
    assert property_lines(cal.serialize(), "EXDATE") == ["EXDATE:20000104T090000Z"]


def test_serialize_rdate_period_keeps_timezone():
    start = datetime.datetime(2000, 1, 4, 9, tzinfo=NEW_YORK)
    cal = multidate_calendar("rdate", [(start, start + HOUR)], value_param="PERIOD")
    assert property_lines(cal.serialize(), "RDATE") == [
        "RDATE;TZID=America/New_York;VALUE=PERIOD:20000104T090000/20000104T100000"
    ]


def test_serialize_mixed_timezones_use_first_timezone():
    """Values are converted to the first value's timezone, keeping their instants."""
    values = [datetime.datetime(2000, 1, 4, 9, tzinfo=NEW_YORK), datetime.datetime(2000, 1, 5, 9, tzinfo=UTC)]
    cal = multidate_calendar("exdate", values)
    assert property_lines(cal.serialize(), "EXDATE") == ["EXDATE;TZID=America/New_York:20000104T090000,20000105T040000"]


def test_serialize_mixed_timezones_first_utc():
    values = [datetime.datetime(2000, 1, 4, 9, tzinfo=UTC), datetime.datetime(2000, 1, 5, 9, tzinfo=NEW_YORK)]
    cal = multidate_calendar("exdate", values)
    assert property_lines(cal.serialize(), "EXDATE") == ["EXDATE:20000104T090000Z,20000105T140000Z"]


@pytest.mark.parametrize("validate", [True, False])
@pytest.mark.parametrize(
    "value, message",
    [
        ([datetime.date(2000, 1, 4), datetime.datetime(2000, 1, 5, 9, tzinfo=UTC)], "same type"),
        (
            [datetime.datetime(2000, 1, 4, 9, tzinfo=UTC), (datetime.datetime(2000, 1, 5, 9, tzinfo=UTC), HOUR)],
            "same type",
        ),
        ([datetime.datetime(2000, 1, 4, 9), datetime.datetime(2000, 1, 5, 9, tzinfo=NEW_YORK)], "floating"),
        ([(datetime.datetime(2000, 1, 4, 9), datetime.datetime(2000, 1, 4, 10, tzinfo=NEW_YORK))], "floating"),
        (["20000104T090000Z"], "must be dates"),
    ],
)
def test_serialize_unwritable_values_always_raise(value, message, validate):
    """These can't be written correctly, so they fail with or without validation."""
    cal = multidate_calendar("rdate", value)
    expected = vobject.base.ValidateError if validate else vobject.base.NativeError
    with pytest.raises(expected, match=message):
        cal.serialize(validate=validate)


@pytest.mark.parametrize("name", ["rdate", "exdate"])
def test_serialize_empty_value(name):
    cal = multidate_calendar(name, [])
    with pytest.raises(vobject.base.ValidateError, match="at least one value"):
        cal.serialize()
    assert property_lines(cal.serialize(validate=False), name.upper()) == [f"{name.upper()}:"]


def test_serialize_exdate_period():
    cal = multidate_calendar("exdate", [(datetime.datetime(2000, 1, 4, 9, tzinfo=UTC), HOUR)])
    with pytest.raises(vobject.base.ValidateError, match="can't be periods"):
        cal.serialize()
    assert property_lines(cal.serialize(validate=False), "EXDATE") == ["EXDATE;VALUE=PERIOD:20000104T090000Z/PT1H"]


@pytest.mark.parametrize(
    "line, message",
    [
        ("EXDATE:", "at least one value"),
        ("RDATE:", "at least one value"),
        ("EXDATE;VALUE=PERIOD:20000104T090000Z/PT1H", "can't be periods"),
        ("EXDATE;VALUE=period:20000104T090000Z/PT1H", "can't be periods"),
    ],
)
def test_parse_multidate_validation(line, message):
    """Parsing is lenient by default, and strict with validate=True."""
    raw = MULTIDATE_HEAD + line + "\r\n" + MULTIDATE_TAIL
    vobject.readOne(raw)
    with pytest.raises(vobject.base.ValidateError, match=message):
        vobject.readOne(raw, validate=True)


def test_parse_valid_multidates_with_validation():
    lines = "RDATE;VALUE=PERIOD:20000104T090000Z/PT1H\r\nEXDATE;VALUE=DATE:20000105\r\n"
    cal = vobject.readOne(MULTIDATE_HEAD + lines + MULTIDATE_TAIL, validate=True)
    assert cal.vevent.rdate.value == [(datetime.datetime(2000, 1, 4, 9, tzinfo=UTC), HOUR)]


@pytest.mark.parametrize(
    "name, value, expected_tzids",
    [
        ("exdate", [datetime.datetime(2000, 1, 4, 9, tzinfo=NEW_YORK)], ["America/New_York"]),
        ("rdate", [(datetime.datetime(2000, 1, 4, 9, tzinfo=NEW_YORK), HOUR)], ["America/New_York"]),
        (
            "exdate",
            [
                datetime.datetime(2000, 1, 4, 9, tzinfo=NEW_YORK),
                datetime.datetime(2000, 1, 5, 9, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
            ],
            ["America/New_York"],
        ),
        ("exdate", [datetime.datetime(2000, 1, 4, 9, tzinfo=UTC)], []),
    ],
)
def test_serialize_multidate_adds_vtimezone(name, value, expected_tzids):
    """A VTIMEZONE is added for the timezone each RDATE or EXDATE is written in, and no others."""
    serialized = multidate_calendar(name, value).serialize()
    assert property_lines(serialized, "TZID") == [f"TZID:{tzid}" for tzid in expected_tzids]
    for tzid in expected_tzids:
        assert f"{name.upper()};TZID={tzid}" in serialized


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

    # zoneinfo
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
