import datetime
import logging
import zoneinfo

import dateutil.rrule
import pytest

import vobject


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


def _multidate_calendar(name, value):
    cal = vobject.iCalendar()
    event = cal.add("vevent")
    event.add("uid").value = "test"
    event.add("dtstart").value = datetime.datetime(2000, 1, 1, 9, tzinfo=vobject.icalendar.utc)
    event.add(name).value = value
    return cal


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
    assert years([(datetime.datetime(2030, 12, 31, 23, tzinfo=utc), datetime.datetime(2031, 1, 2, 1, tzinfo=utc))]) == [
        2030,
        2031,
    ]


@pytest.mark.parametrize(
    "name, value, check_local, offset_hours",
    [
        (
            "exdate",
            [datetime.datetime(1995, 7, 15, 12, tzinfo=zoneinfo.ZoneInfo("America/Chicago"))],
            datetime.datetime(1995, 7, 15, 12),
            -5,
        ),
        (
            "rdate",
            [
                (
                    datetime.datetime(1995, 7, 15, 12, tzinfo=zoneinfo.ZoneInfo("America/Chicago")),
                    datetime.timedelta(hours=1),
                )
            ],
            datetime.datetime(1995, 7, 15, 12),
            -5,
        ),
        (
            "rdate",
            [
                (
                    datetime.datetime(2030, 12, 31, 12, tzinfo=zoneinfo.ZoneInfo("Asia/Jerusalem")),
                    datetime.datetime(2031, 4, 1, 12, tzinfo=zoneinfo.ZoneInfo("Asia/Jerusalem")),
                )
            ],
            datetime.datetime(2031, 4, 1, 12),
            3,
        ),
    ],
)
def test_generated_vtimezone_covers_multidate_year(name, value, check_local, offset_hours):
    """
    A VTIMEZONE generated for an EXDATE or RDATE list covers its datetimes' years.
    """
    serialized = _multidate_calendar(name, value).serialize()
    tzinfo = _stored_vtimezone_tzinfo(serialized)
    assert check_local.replace(tzinfo=tzinfo).utcoffset() == datetime.timedelta(hours=offset_hours)


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


def _dateutil_accepts_rrule_parameters():
    try:
        dateutil.rrule.rrulestr("RRULE;X-TEST=yes:FREQ=YEARLY;COUNT=1", dtstart=datetime.datetime(2000, 1, 1))
    except ValueError:
        return False
    return True


@pytest.mark.skipif(
    not _dateutil_accepts_rrule_parameters(),
    reason="this dateutil rejects any RRULE parameter, with or without the rewrite",
)
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


def test_generated_vtimezone_falls_back_to_default_range(monkeypatch, caplog):
    """
    If settzinfo fails for the extended range, the default range is used and a warning is logged.
    """
    original = vobject.icalendar.TimezoneComponent.settzinfo

    def settzinfo(self, tzinfo, start=2000, end=2030):
        if (start, end) != (2000, 2030):
            raise OverflowError("date value out of range")
        return original(self, tzinfo, start, end)

    monkeypatch.setattr(vobject.icalendar.TimezoneComponent, "settzinfo", settzinfo)
    with caplog.at_level(logging.WARNING, logger=vobject.base.logger.name):
        serialized = vobject.readOne(_tzid_only_event("America/Chicago", "19950715T120000")).serialize()
    default = vobject.icalendar.TimezoneComponent(tzinfo=vobject.icalendar.getTzid("America/Chicago")).serialize()
    assert default in serialized
    assert any("America/Chicago" in r.message and "1994-2030" in r.message for r in caplog.records)
