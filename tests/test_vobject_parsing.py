import datetime

import pytest

import vobject

silly_test_text = (
    "sillyname:name\r\n"
    "profile:sillyprofile\r\n"
    "stuff:folded\r\n"
    " line\r\n"
    "morestuff;asinine:this line is not folded, but in practice probably ought to be, as it is exceptionally long, "
    "and moreover demonstratively stupid\r\n"
)

standard_test_text = (
    "BEGIN:VCALENDAR\r\n"
    "CALSCALE:GREGORIAN\r\n"
    "X-WR-TIMEZONE;VALUE=TEXT:US/Pacific\r\n"
    "METHOD:PUBLISH\r\n"
    "PRODID:-//Apple Computer\\, Inc//iCal 1.0//EN\r\n"
    "X-WR-CALNAME;VALUE=TEXT:Example\r\n"
    "VERSION:2.0\r\n"
    "BEGIN:VEVENT\r\n"
    "SEQUENCE:5\r\n"
    "DTSTART;TZID=US/Pacific:20021028T140000\r\n"
    "RRULE:FREQ=Weekly;COUNT=10\r\n"
    "DTSTAMP:20021028T011706Z\r\n"
    "SUMMARY:Coffee with Jason\r\n"
    "UID:EC9439B1-FF65-11D6-9973-003065F99D04\r\n"
    "DTEND;TZID=US/Pacific:20021028T150000\r\n"
    "BEGIN:VALARM\r\n"
    "TRIGGER;VALUE=DURATION:-P1D\r\n"
    "ACTION:DISPLAY\r\n"
    "DESCRIPTION:Event reminder\\, with comma\\nand line feed\r\n"
    "END:VALARM\r\n"
    "END:VEVENT\r\n"
    "BEGIN:VTIMEZONE\r\n"
    "X-LIC-LOCATION:Random location\r\n"
    "TZID:US/Pacific\r\n"
    "LAST-MODIFIED:19870101T000000Z\r\n"
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
    "END:VCALENDAR\r\n"
)

bad_stream = (
    "BEGIN:VCALENDAR\r\n"
    "CALSCALE:GREGORIAN\r\n"
    "X-WR-TIMEZONE;VALUE=TEXT:US/Pacific\r\n"
    "METHOD:PUBLISH\r\n"
    "PRODID:-//Apple Computer\\, Inc//iCal 1.0//EN\r\n"
    "X-WR-CALNAME;VALUE=TEXT:Example\r\n"
    "VERSION:2.0\r\n"
    "BEGIN:VEVENT\r\n"
    "DTSTART:20021028T140000Z\r\n"
    "BEGIN:VALARM\r\n"
    "TRIGGER:a20021028120000\r\n"
    "ACTION:DISPLAY\r\n"
    "DESCRIPTION:This trigger has a nonsensical value\r\n"
    "END:VALARM\r\n"
    "END:VEVENT\r\n"
    "END:VCALENDAR\r\n"
)

bad_line = (
    "BEGIN:VCALENDAR\r\n"
    "METHOD:PUBLISH\r\n"
    "VERSION:2.0\r\n"
    "BEGIN:VEVENT\r\n"
    "DTSTART:19870405T020000\r\n"
    "X-BAD/SLASH:TRUE\r\n"
    "X-BAD_UNDERSCORE:TRUE\r\n"
    "UID:EC9439B1-FF65-11D6-9973-003065F99D04\r\n"
    "END:VEVENT\r\n"
    "END:VCALENDAR\r\n"
)

quoted_printable = (
    "BEGIN:VCARD\r\n"
    "VERSION:2.1\r\n"
    "N;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:=E9=BB=84;=E4=B8=96=E5=8B=87;;;\r\n"
    "FN;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:=E9=BB=84=E4=B8=96=E5=8B=87\r\n"
    "TEL;CELL:15810139237\r\n"
    "TEL;WORK:01088520374\r\n"
    "ADR;HOME;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:;;;=E5=8C=97=E4=BA=AC=20=E4=B8=B0=E5=8F=B0=E5=8C=BA;;;\r\n"
    "URL;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:=68=74=74=70=3A=2F=2F=77=65=69=62=6F=2E=63=6F=6D=2F=33=30=39=34=39=30="
    "\r\n"
    "=30=34=33=33=3F=E9=97=AA=E9=97=AA=48=E7=BA=A2=E6=98=9F\r\n"
    "END:VCARD\r\n"
)


def test_readOne():
    """
    Test reading first component of ics
    """
    cal = silly_test_text
    silly = vobject.base.readOne(cal)
    assert (
        str(silly)
        == "<SILLYPROFILE| [<MORESTUFF{}this line is not folded, but in practice probably ought to be, as it is "
        "exceptionally long, and moreover demonstratively stupid>, <SILLYNAME{}name>, <STUFF{}foldedline>]>"
    )
    assert str(silly.stuff) == "<STUFF{}foldedline>"


def test_importing():
    """
    Test importing ics
    """
    cal = standard_test_text
    c = vobject.base.readOne(cal, validate=True)
    assert str(c.vevent.valarm.trigger) == "<TRIGGER{}-1 day, 0:00:00>"
    assert str(c.vevent.dtstart.value) == "2002-10-28 14:00:00-08:00"
    assert isinstance(c.vevent.dtstart.value, datetime.datetime)
    assert str(c.vevent.dtend.value) == "2002-10-28 15:00:00-08:00"
    assert isinstance(c.vevent.dtend.value, datetime.datetime)
    assert c.vevent.dtstamp.value == datetime.datetime(2002, 10, 28, 1, 17, 6, tzinfo=datetime.timezone.utc)

    vevent = c.vevent.transformFromNative()
    assert str(vevent.rrule) == "<RRULE{}FREQ=Weekly;COUNT=10>"


def test_bad_stream():
    """
    Test bad ics stream
    """
    with pytest.raises(vobject.base.ParseError):
        vobject.base.readOne(bad_stream)


def test_bad_line():
    """
    Test bad line in ics file
    """
    with pytest.raises(vobject.base.ParseError):
        vobject.base.readOne(bad_line)

    cal = vobject.base.readOne(bad_line, ignoreUnreadable=True)
    assert str(cal.vevent.x_bad_underscore) == "<X-BAD-UNDERSCORE{}TRUE>"


def test_parse_params():
    """
    Test parsing parameters
    """
    assert vobject.base.parseParams(';ALTREP="http://www.wiz.org"') == [["ALTREP", "http://www.wiz.org"]]
    assert vobject.base.parseParams(';ALTREP="http://www.wiz.org;;",Blah,Foo;NEXT=Nope;BAR') == [
        ["ALTREP", "http://www.wiz.org;;", "Blah", "Foo"],
        ["NEXT", "Nope"],
        ["BAR"],
    ]


def test_quoted_printable():
    """
    The use of QUOTED-PRINTABLE encoding
    """
    vobjs = vobject.base.readComponents(quoted_printable, allowQP=True)
    for vo in vobjs:
        assert vo is not None
