import copy
import datetime
import pickle
import zoneinfo

import pytest

import vobject

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


def test_tzid_fallback_recurrence_across_dst():
    ics = (
        "BEGIN:VCALENDAR\r\n"
        "VERSION:2.0\r\n"
        "PRODID:-//Test//EN\r\n"
        "BEGIN:VEVENT\r\n"
        "UID:tzid-only-weekly\r\n"
        "DTSTART;TZID=America/Chicago:20270301T090000\r\n"
        "RRULE:FREQ=WEEKLY;COUNT=4\r\n"
        "SUMMARY:Weekly DST\r\n"
        "END:VEVENT\r\n"
        "END:VCALENDAR\r\n"
    )
    cal = vobject.base.readOne(ics)
    utc_hours = [dt.astimezone(datetime.timezone.utc).strftime("%Y%m%dT%H%M") for dt in cal.vevent.getrruleset()]
    assert utc_hours == ["20270301T1500", "20270308T1500", "20270315T1400", "20270322T1400"]

    fall_ics = (
        "BEGIN:VCALENDAR\r\n"
        "VERSION:2.0\r\n"
        "PRODID:-//Test//EN\r\n"
        "BEGIN:VEVENT\r\n"
        "UID:tzid-only-fall\r\n"
        "DTSTART;TZID=America/Chicago:20271025T090000\r\n"
        "RRULE:FREQ=WEEKLY;COUNT=4\r\n"
        "SUMMARY:Fall Back\r\n"
        "END:VEVENT\r\n"
        "END:VCALENDAR\r\n"
    )
    fall_cal = vobject.base.readOne(fall_ics)
    fall_utc = [dt.astimezone(datetime.timezone.utc).strftime("%Y%m%dT%H%M") for dt in fall_cal.vevent.getrruleset()]
    assert fall_utc == ["20271025T1400", "20271101T1400", "20271108T1500", "20271115T1500"]


def test_tzid_fallback_does_not_poison_vtimezone():
    bare_ics = (
        "BEGIN:VCALENDAR\r\n"
        "VERSION:2.0\r\n"
        "PRODID:-//Test//EN\r\n"
        "BEGIN:VEVENT\r\n"
        "UID:bare-chicago\r\n"
        "DTSTART;TZID=America/Chicago:20270301T090000\r\n"
        "SUMMARY:Bare TZID\r\n"
        "END:VEVENT\r\n"
        "END:VCALENDAR\r\n"
    )
    vobject.base.readOne(bare_ics)
    assert vobject.icalendar.getTzid("America/Chicago", smart=False) is None

    vtz_ics = (
        "BEGIN:VCALENDAR\r\n"
        "VERSION:2.0\r\n"
        "PRODID:-//Test//EN\r\n"
        "BEGIN:VTIMEZONE\r\n"
        "TZID:America/Chicago\r\n"
        "BEGIN:STANDARD\r\n"
        "DTSTART:20071104T020000\r\n"
        "RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU\r\n"
        "TZOFFSETFROM:-0500\r\n"
        "TZOFFSETTO:-0600\r\n"
        "TZNAME:CST\r\n"
        "END:STANDARD\r\n"
        "BEGIN:DAYLIGHT\r\n"
        "DTSTART:20070311T020000\r\n"
        "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU\r\n"
        "TZOFFSETFROM:-0600\r\n"
        "TZOFFSETTO:-0500\r\n"
        "TZNAME:CDT\r\n"
        "END:DAYLIGHT\r\n"
        "END:VTIMEZONE\r\n"
        "BEGIN:VEVENT\r\n"
        "UID:vtz-chicago\r\n"
        "DTSTART;TZID=America/Chicago:20270301T090000\r\n"
        "RRULE:FREQ=WEEKLY;COUNT=4\r\n"
        "SUMMARY:With VTIMEZONE\r\n"
        "END:VEVENT\r\n"
        "END:VCALENDAR\r\n"
    )
    cal = vobject.base.readOne(vtz_ics)
    assert not isinstance(cal.vevent.dtstart.value.tzinfo, zoneinfo.ZoneInfo)
    utc_hours = [dt.astimezone(datetime.timezone.utc).strftime("%Y%m%dT%H%M") for dt in cal.vevent.getrruleset()]
    assert utc_hours == ["20270301T1500", "20270308T1500", "20270315T1400", "20270322T1400"]


def test_vtimezone_scoped_per_calendar():
    cal1_ics = (
        "BEGIN:VCALENDAR\r\n"
        "VERSION:2.0\r\n"
        "PRODID:-//Test//EN\r\n"
        "BEGIN:VTIMEZONE\r\n"
        "TZID:CustomTestZone\r\n"
        "BEGIN:STANDARD\r\n"
        "DTSTART:20000101T000000\r\n"
        "TZOFFSETFROM:+0200\r\n"
        "TZOFFSETTO:+0200\r\n"
        "TZNAME:CTZ1\r\n"
        "END:STANDARD\r\n"
        "END:VTIMEZONE\r\n"
        "BEGIN:VEVENT\r\n"
        "UID:custom-1\r\n"
        "DTSTART;TZID=CustomTestZone:20270601T120000\r\n"
        "END:VEVENT\r\n"
        "END:VCALENDAR\r\n"
    )
    cal2_ics = (
        "BEGIN:VCALENDAR\r\n"
        "VERSION:2.0\r\n"
        "PRODID:-//Test//EN\r\n"
        "BEGIN:VTIMEZONE\r\n"
        "TZID:CustomTestZone\r\n"
        "BEGIN:STANDARD\r\n"
        "DTSTART:20000101T000000\r\n"
        "TZOFFSETFROM:-0400\r\n"
        "TZOFFSETTO:-0400\r\n"
        "TZNAME:CTZ2\r\n"
        "END:STANDARD\r\n"
        "END:VTIMEZONE\r\n"
        "BEGIN:VEVENT\r\n"
        "UID:custom-2\r\n"
        "DTSTART;TZID=CustomTestZone:20270601T120000\r\n"
        "END:VEVENT\r\n"
        "END:VCALENDAR\r\n"
    )
    cal1 = vobject.base.readOne(cal1_ics)
    cal2 = vobject.base.readOne(cal2_ics)
    assert cal1.vevent.dtstart.value.utcoffset() == datetime.timedelta(hours=2)
    assert cal2.vevent.dtstart.value.utcoffset() == datetime.timedelta(hours=-4)
    assert vobject.icalendar.getTzid("CustomTestZone", smart=False) is None
    assert "TZOFFSETTO:+0200" in cal1.serialize()
    assert "TZOFFSETTO:-0400" in cal2.serialize()


@pytest.mark.parametrize("bad_tzid", [None, "", "America", "Nope/Zone", "../etc/passwd", "A" * 300])
def test_tzid_fallback_invalid_names(bad_tzid):
    assert vobject.icalendar.getTzid(bad_tzid) is None


def test_tzid_fallback_historical_and_irregular_zones():
    chicago_1995 = vobject.base.readOne(
        "BEGIN:VCALENDAR\r\n"
        "VERSION:2.0\r\n"
        "PRODID:-//Test//EN\r\n"
        "BEGIN:VEVENT\r\n"
        "UID:chicago-1995\r\n"
        "DTSTART;TZID=America/Chicago:19950715T120000\r\n"
        "END:VEVENT\r\n"
        "END:VCALENDAR\r\n"
    )
    assert chicago_1995.vevent.dtstart.value.astimezone(datetime.timezone.utc) == datetime.datetime(
        1995, 7, 15, 17, 0, tzinfo=datetime.timezone.utc
    )

    jerusalem_2027 = vobject.base.readOne(
        "BEGIN:VCALENDAR\r\n"
        "VERSION:2.0\r\n"
        "PRODID:-//Test//EN\r\n"
        "BEGIN:VEVENT\r\n"
        "UID:jerusalem-2027\r\n"
        "DTSTART;TZID=Asia/Jerusalem:20270326T120000\r\n"
        "END:VEVENT\r\n"
        "END:VCALENDAR\r\n"
    )
    assert jerusalem_2027.vevent.dtstart.value.astimezone(datetime.timezone.utc) == datetime.datetime(
        2027, 3, 26, 9, 0, tzinfo=datetime.timezone.utc
    )


def test_zoneinfo_vtimezone_serialization():
    cal = vobject.base.Component("VCALENDAR")
    cal.setBehavior(vobject.icalendar.VCalendar2_0)
    ev = cal.add("vevent")
    ev.add("dtstart").value = datetime.datetime(2008, 10, 12, 9, tzinfo=zoneinfo.ZoneInfo("US/Eastern"))
    serialized = cal.serialize()
    assert us_eastern.replace("\r\n", "\n") in serialized.replace("\r\n", "\n")

    chicago = vobject.icalendar.TimezoneComponent(tzinfo=zoneinfo.ZoneInfo("America/Chicago")).serialize()
    assert "TZID:America/Chicago" in chicago
    assert "DTSTART:20070311T020000" in chicago
    assert "DTSTART:20071104T020000" in chicago
    assert "TZOFFSETFROM:-0600" in chicago
    assert "TZOFFSETTO:-0500" in chicago
    assert "TZOFFSETFROM:-0500" in chicago
    assert "TZOFFSETTO:-0600" in chicago


def test_duplicate_and_pickle_preserve_vtimezone_scoping():
    ics = (
        "BEGIN:VCALENDAR\r\n"
        "VERSION:2.0\r\n"
        "PRODID:-//Test//EN\r\n"
        "BEGIN:VTIMEZONE\r\n"
        "TZID:America/Chicago\r\n"
        "BEGIN:STANDARD\r\n"
        "DTSTART:19700101T000000\r\n"
        "TZOFFSETFROM:+0100\r\n"
        "TZOFFSETTO:+0100\r\n"
        "TZNAME:TEST\r\n"
        "END:STANDARD\r\n"
        "END:VTIMEZONE\r\n"
        "BEGIN:VEVENT\r\n"
        "UID:dup-1\r\n"
        "DTSTART;TZID=America/Chicago:20260101T120000\r\n"
        "END:VEVENT\r\n"
        "END:VCALENDAR\r\n"
    )
    cal = vobject.base.readOne(ics)

    dup = cal.duplicate(cal)
    dup.vevent.dtstart.value = "20260101T120000"
    dup.vevent.dtstart.isNative = False
    dup.vevent.dtstart.params = {"TZID": ["America/Chicago"]}
    dup.transformChildrenToNative()
    assert dup.vevent.dtstart.value.utcoffset() == datetime.timedelta(hours=1)

    tz_only = vobject.base.readOne(ics)
    del tz_only.contents["vevent"]
    assert copy.deepcopy(tz_only).vtimezone.tzid.value == "America/Chicago"
    assert pickle.loads(pickle.dumps(tz_only)).vtimezone.tzid.value == "America/Chicago"


def test_tzid_fallback_case_insensitive():
    tz = vobject.icalendar.getTzid("america/chicago")
    assert isinstance(tz, zoneinfo.ZoneInfo)
    assert tz.key == "America/Chicago"


def test_tzinfo_eq_zoneinfo_and_pytz():
    try:
        import pytz
    except ImportError:
        pytest.skip("pytz not installed")

    for name in ("America/Chicago", "Australia/Sydney", "Asia/Jerusalem"):
        zi = zoneinfo.ZoneInfo(name)
        pz = pytz.timezone(name)
        assert vobject.icalendar.tzinfo_eq(zi, pz, 2026, 2027) is True
        assert vobject.icalendar.tzinfo_eq(pz, zi, 2026, 2027) is True


def test_zoneinfo_nuuk_historical_until_roundtrip():
    ics = (
        "BEGIN:VCALENDAR\r\n"
        "VERSION:2.0\r\n"
        "PRODID:-//Test//EN\r\n"
        "BEGIN:VEVENT\r\n"
        "UID:nuuk-2026\r\n"
        "DTSTART;TZID=America/Nuuk:20261030T120000\r\n"
        "RRULE:FREQ=DAILY;COUNT=5\r\n"
        "END:VEVENT\r\n"
        "END:VCALENDAR\r\n"
    )
    cal = vobject.base.readOne(ics)
    before = [dt.utcoffset() for dt in cal.vevent.getrruleset()]
    reparsed = vobject.base.readOne(cal.serialize())
    after = [dt.utcoffset() for dt in reparsed.vevent.getrruleset()]
    assert before == after
    assert after[-1] == datetime.timedelta(hours=-2)
