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

    assert str(cal) == "<VCALENDAR| [<VEVENT| [<SUMMARY{'BLAH': ['hi!']}[]Bastille Day Party>]>]>"
    assert str(cal.vevent.summary) == "<SUMMARY{'BLAH': ['hi!']}[]Bastille Day Party>"


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


def test_contentline_parameter_getattr():
    cl = vobject.base.textLineToContentLine("NAME;P1=P1V1,P1V2;P2=P2V1;P3;P4:VALUE\r\n")
    assert cl.p1_param == "P1V1"
    assert cl.p2_param == "P2V1"
    assert cl.p3_param == "P3"
    assert cl.p4_param == "P4"
    assert cl.p1_paramlist == ["P1V1", "P1V2"]
    assert cl.p2_paramlist == ["P2V1"]
    assert cl.p3_paramlist is None
    assert cl.p4_paramlist is None


def test_contentline_parameter_setattr():
    cl = vobject.base.textLineToContentLine("NAME:VALUE\r\n")
    assert len(cl.params) == 0
    assert len(cl.singletonparams) == 0

    cl.p1_param = None
    assert len(cl.singletonparams) == 1
    assert cl.singletonparams[0] == "P1"

    cl.p2_param = None
    assert len(cl.singletonparams) == 2
    assert cl.singletonparams[0] == "P1"
    assert cl.singletonparams[1] == "P2"

    cl.p3_param = "P3V1"
    assert len(cl.params) == 1
    assert "P3" in cl.params
    assert cl.params["P3"] == ["P3V1"]

    cl.p3_param = "P3V2"
    assert len(cl.params) == 1
    assert "P3" in cl.params
    assert cl.params["P3"] == ["P3V2"]

    cl.p3_param = ["P3V1", "P3V2"]
    assert len(cl.params), 1
    assert "P3" in cl.params, True
    assert cl.params["P3"], ["P3V1", "P3V2"]

    cl.p4_paramlist = ["P4V1", "P4V2"]
    assert len(cl.params), 2
    assert "P4" in cl.params, True
    assert cl.params["P4"], ["P4V1", "P4V2"]

    with pytest.raises(vobject.base.VObjectError) as error:
        cl.p4_paramlist = None
    assert error.value.msg == "Cannot set standalone parameter using _paramlist suffix"
    assert cl.params["P4"] == ["P4V1", "P4V2"]

    with pytest.raises(vobject.base.VObjectError) as error:
        cl.p4_paramlist = ("no", "nein", "non", "nyet")
    assert error.value.msg == "Parameter list set to a non-list"
    assert cl.params["P4"] == ["P4V1", "P4V2"]


def test_contentline_parameter_delattr():
    cl = vobject.base.textLineToContentLine("NAME;P1=P1V1,P1V2;P2=P2V1;P3;P4:VALUE\r\n")
    assert len(cl.params) == 2
    assert "P1" in cl.params
    assert cl.params["P1"] == ["P1V1", "P1V2"]
    assert "P2" in cl.params
    assert cl.params["P2"] == ["P2V1"]

    assert len(cl.singletonparams) == 2
    assert "P3" in cl.singletonparams
    assert "P4" in cl.singletonparams

    del cl.p4_param
    assert len(cl.singletonparams) == 1
    assert "P3" in cl.singletonparams
    assert "P4" not in cl.singletonparams

    with pytest.raises(AttributeError) as error:
        del cl.p4_param
    assert error.value.args[0] == "P4"

    with pytest.raises(vobject.base.VObjectError):
        del cl.p3_paramlist

    del cl.p3_param
    assert len(cl.singletonparams) == 0

    del cl.p1_param
    assert len(cl.params) == 1

    del cl.p2_paramlist
    assert len(cl.params) == 0
