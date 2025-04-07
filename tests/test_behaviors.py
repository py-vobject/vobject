import datetime

import vobject


def test_general_behavior():
    """
    Tests for behavior registry, getting and creating a behavior.
    """
    # test get_behavior
    behavior = vobject.base.getBehavior("VCALENDAR")
    assert str(behavior) == "<class 'vobject.icalendar.VCalendar2_0'>"
    assert behavior.isComponent
    assert vobject.base.getBehavior("invalid_name") is None

    # test for ContentLine (not a component)
    non_component_behavior = vobject.base.getBehavior("RDATE")
    assert not non_component_behavior.isComponent


def test_multi_date_behavior():
    """
    Test MultiDateBehavior
    """
    parse_r_date = vobject.icalendar.MultiDateBehavior.transformToNative

    expected = (
        "<RDATE{'VALUE': ['DATE']}[datetime.date(1997, 3, 4), datetime.date(1997, 5, 4), "
        "datetime.date(1997, 7, 4), datetime.date(1997, 9, 4)]>"
    )
    result = str(
        parse_r_date(vobject.base.textLineToContentLine("RDATE;VALUE=DATE:19970304,19970504,19970704,19970904"))
    )
    assert result == expected

    expected = (
        "<RDATE{'VALUE': ['PERIOD']}[(datetime.datetime(1996, 4, 3, 2, 0, tzinfo=tzutc()), "
        "datetime.datetime(1996, 4, 3, 4, 0, tzinfo=tzutc())), "
        "(datetime.datetime(1996, 4, 4, 1, 0, tzinfo=tzutc()), datetime.timedelta(seconds=10800))]>"
    )
    result = str(
        parse_r_date(
            vobject.base.textLineToContentLine(
                "RDATE;VALUE=PERIOD:19960403T020000Z/19960403T040000Z,19960404T010000Z/PT3H"
            )
        )
    )
    assert result == expected


def test_period_behavior():
    """
    Test PeriodBehavior
    """
    two_hours = datetime.timedelta(hours=2)

    line = vobject.base.ContentLine("test", [], "", isNative=True)
    line.behavior = vobject.icalendar.PeriodBehavior

    line.value = [(datetime.datetime(2006, 2, 16, 10), two_hours)]
    assert line.transformFromNative().value == "20060216T100000/PT2H"
    expected = [(datetime.datetime(2006, 2, 16, 10, 0), datetime.timedelta(0, 7200))]
    assert line.transformToNative().value == expected

    line.value.append((datetime.datetime(2006, 5, 16, 10), two_hours))
    assert line.serialize().strip() == "TEST:20060216T100000/PT2H,20060516T100000/PT2H"
