import io

import pytest

import vobject

ics_text = (
    "BEGIN:VCALENDAR\r\n"
    "BEGIN:VEVENT\r\n"
    "SUMMARY;blah=hi!:Bastille Day Party\r\n"
    "END:VEVENT\r\n"
    "END:VCALENDAR\r\n"
)


def test_read_components():
    """
    Test if reading components correctly
    """
    cal = next(vobject.readComponents(io.StringIO(ics_text)))

    assert str(cal) == "<VCALENDAR| [<VEVENT| [<SUMMARY{'BLAH': ['hi!']}Bastille Day Party>]>]>"
    assert str(cal.vevent.summary) == "<SUMMARY{'BLAH': ['hi!']}Bastille Day Party>"


def test_parse_line():
    """
    Test line parsing
    """
    assert vobject.base.parseLine("BLAH:") == ("BLAH", [], "", None)
    assert vobject.base.parseLine("RDATE:VALUE=DATE:19970304,19970504,19970704,19970904") == (
        "RDATE",
        [],
        "VALUE=DATE:19970304,19970504,19970704,19970904",
        None,
    )
    assert vobject.base.parseLine(
        'DESCRIPTION;ALTREP="http://www.wiz.org":The Fall 98 Wild Wizards Conference - - Las Vegas, NV, USA'
    ) == (
        "DESCRIPTION",
        [["ALTREP", "http://www.wiz.org"]],
        "The Fall 98 Wild Wizards Conference - - Las Vegas, NV, USA",
        None,
    )
    assert vobject.base.parseLine("EMAIL;PREF;INTERNET:john@nowhere.com") == (
        "EMAIL",
        [["PREF"], ["INTERNET"]],
        "john@nowhere.com",
        None,
    )
    assert vobject.base.parseLine('EMAIL;TYPE="blah",hah;INTERNET="DIGI",DERIDOO:john@nowhere.com') == (
        "EMAIL",
        [["TYPE", "blah", "hah"], ["INTERNET", "DIGI", "DERIDOO"]],
        "john@nowhere.com",
        None,
    )
    assert vobject.base.parseLine("item1.ADR;type=HOME;type=pref:;;Reeperbahn 116;Hamburg;;20359;") == (
        "ADR",
        [["type", "HOME"], ["type", "pref"]],
        ";;Reeperbahn 116;Hamburg;;20359;",
        "item1",
    )
    with pytest.raises(vobject.base.ParseError):
        vobject.base.parseLine(":")
