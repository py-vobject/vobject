import datetime
import io
import json

import dateutil

import vobject

simple_2_0_test = (
    "BEGIN:VCALENDAR\r\n"
    "VERSION:2.0\r\n"
    "PRODID:-//PYVOBJECT//NONSGML Version %s//EN\r\n"
    "BEGIN:VEVENT\r\n"
    "UID:Not very random UID\r\n"
    "DTSTART:20060509T000000\r\n"
    "ATTENDEE;CN=Fröhlich:mailto:froelich@example.com\r\n"
    "CREATED:20060101T180000Z\r\n"
    "DESCRIPTION:Test event\r\n"
    "DTSTAMP:20170626T000000Z\r\n"
    "END:VEVENT\r\n"
    "END:VCALENDAR\r\n"
)

us_pacific = (
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
)

utf8_test = (
    "BEGIN:VCALENDAR\r\n"
    "METHOD:PUBLISH\r\n"
    "CALSCALE:GREGORIAN\r\n"
    "PRODID:-//EVDB//www.evdb.com//EN\r\n"
    "VERSION:2.0\r\n"
    "X-WR-CALNAME:EVDB Event Feed\r\n"
    "BEGIN:VEVENT\r\n"
    "DTSTART:20060922T000100Z\r\n"
    "DTEND:20060922T050100Z\r\n"
    "DTSTAMP:20050914T163414Z\r\n"
    "SUMMARY:The title こんにちはキティ\r\n"
    "DESCRIPTION:hello\\nHere is a description\\n\\n\\nこんにちはキティ\r\n"
    "	\\n\\n\\n\\nZwei Java-schwere Entwicklerpositionen und irgendeine Art sond\r\n"
    "	erbar-klingende Netzsichtbarmachungöffnung\\, an einer interessanten F\r\n"
    "	irma im Gebäude\\, in dem ich angerufenen Semantic Research bearbeite.\r\n"
    "	 1. Zauberer Des Semantica Software Engineer 2. Älterer Semantica Sof\r\n"
    "	tware-Englisch-3. Graph/Semantica Netz-Visualization/Navigation Sie ei\r\n"
    "	ngestufte Software-Entwicklung für die Regierung. Die Firma ist stark\r\n"
    "	 und die Projekte sind sehr kühl und schließen irgendeinen Spielraum\r\n"
    "	 ein. Wenn ich Ihnen irgendwie mehr erkläre\\, muß ich Sie töten. Ps\r\n"
    "	. Tat schnell -- jemand ist\\, wenn es hier interviewt\\, wie ich dieses\r\n"
    "	 schreibe. Er schaut intelligent (er trägt Kleidhosen) Semantica Soft\r\n"
    "	ware Engineer FIRMA: Semantische Forschung\\, Inc. REPORTS ZU: Vizeprä\r\n"
    "	sident\\, Produkt-Entwicklung POSITION: San Diego (Pint Loma) WEB SITE:\r\n"
    "	 www.semanticresearch.com email: dorie@semanticresearch.com FIRMA-HINT\r\n"
    "	ERGRUND Semantische Forschung ist der führende Versorger der semantis\r\n"
    "	cher Netzwerkanschluß gegründeten nicht linearen Wissen Darstellung \r\n"
    "	Werkzeuge. Die Firma stellt diese Werkzeuge zum Intel\\, zur reg.\\, zum\r\n"
    "	 EDU und zu den kommerziellen Märkten zur Verfügung. BRINGEN SIE ZUS\r\n"
    "	AMMENFASSUNG IN POSITION Semantische Forschung\\, Inc. basiert in San D\r\n"
    "	iego\\, Ca im alten realen Weltsan Diego Haus...\\, das wir den Weltbest\r\n"
    "	en Platz haben zum zu arbeiten. Wir suchen nach Superstarentwicklern\\,\r\n"
    "	 um uns in der fortfahrenden Entwicklung unserer Semantica Produktseri\r\n"
    "	e zu unterstützen.\r\n"
    "LOCATION:こんにちはキティ\r\n"
    "SEQUENCE:0\r\n"
    "UID:E0-001-000276068-2\r\n"
    "END:VEVENT\r\n"
    "END:VCALENDAR\r\n"
)

journal = (
    "BEGIN:VJOURNAL\r\n"
    "UID:19970901T130000Z-123405@example.com\r\n"
    "DTSTAMP:19970901T130000Z\r\n"
    "DTSTART;VALUE=DATE:19970317\r\n"
    "SUMMARY:Staff meeting minutes\r\n"
    "DESCRIPTION:1. Staff meeting: Participants include Joe\\,\r\n"
    "  Lisa\\, and Bob. Aurora project plans were reviewed.\r\n"
    "  There is currently no budget reserves for this project.\r\n"
    "  Lisa will escalate to management. Next meeting on Tuesday.\\n\r\n"
    " 2. Telephone Conference: ABC Corp. sales representative\r\n"
    "  called to discuss new printer. Promised to get us a demo by\r\n"
    "  Friday.\\n3. Henry Miller (Handsoff Insurance): Car was\r\n"
    "  totaled by tree. Is looking into a loaner car. 555-2323\r\n"
    "  (tel).\r\n"
    "END:VJOURNAL\r\n"
)


def test_scratch_build():
    """
    CreateCalendar 2.0 format from scratch
    """
    cal = vobject.base.newFromBehavior("vcalendar", "2.0")
    cal.add("vevent")
    cal.vevent.add("dtstart").value = datetime.datetime(2006, 5, 9)
    cal.vevent.add("description").value = "Test event"
    cal.vevent.add("created").value = datetime.datetime(
        2006, 1, 1, 10, tzinfo=dateutil.tz.tzical(io.StringIO(us_pacific)).get("US/Pacific")
    )
    cal.vevent.add("uid").value = "Not very random UID"
    cal.vevent.add("dtstamp").value = datetime.datetime(2017, 6, 26, 0, tzinfo=datetime.timezone.utc)

    cal.vevent.add("attendee").value = "mailto:froelich@example.com"
    cal.vevent.attendee.params["CN"] = ["Fröhlich"]

    # Note we're normalizing line endings, because no one got time for that.
    assert cal.serialize().replace("\r\n", "\n") == simple_2_0_test.replace("\r\n", "\n") % vobject.VERSION


def test_unicode():
    """
    Test unicode characters
    """
    vevent = vobject.base.readOne(utf8_test).vevent
    vevent2 = vobject.base.readOne(vevent.serialize())

    assert str(vevent) == str(vevent2)
    assert vevent.summary.value == "The title こんにちはキティ"


def test_wrapping():
    """
    Should support input file with a long text field covering multiple lines
    """
    vobj = vobject.base.readOne(journal)
    vjournal = vobject.base.readOne(vobj.serialize())
    assert "Joe, Lisa, and Bob" in vjournal.description.value
    assert "Tuesday.\n2." in vjournal.description.value


def test_multiline():
    """
    Multi-text serialization test
    """
    category = vobject.base.newFromBehavior("categories")
    category.value = ["Random category"]
    assert category.serialize().strip() == "CATEGORIES:Random category"

    category.value.append("Other category")
    assert category.serialize().strip() == "CATEGORIES:Random category,Other category"


def test_semicolon_separated():
    """
    Semi-colon separated multi-text serialization test
    """
    request_status = vobject.base.newFromBehavior("request-status")
    request_status.value = ["5.1", "Service unavailable"]
    assert request_status.serialize().strip() == "REQUEST-STATUS:5.1;Service unavailable"


def test_unicode_multiline():
    """
    Test multiline unicode characters
    """
    cal = vobject.iCalendar()
    cal.add("method").value = "REQUEST"
    cal.add("vevent")
    cal.vevent.add("created").value = datetime.datetime.now()
    cal.vevent.add("summary").value = "Классное событие"
    cal.vevent.add("description").value = (
        "Классное событие Классное событие Классное событие Классное событие Классное событие Классsdssdное событие"
    )

    # json tries to encode as utf-8 and it would break if some chars could not be encoded
    json.dumps(cal.serialize())


def test_ical_to_hcal():
    """
    Serializing iCalendar to hCalendar.

    Since Hcalendar is experimental and the behavior doesn't seem to want to load,
    This test will have to wait.


    tzs = dateutil.tz.tzical("test_files/timezones.ics")
    cal = base.newFromBehavior('hcalendar')
    self.assertEqual(
        str(cal.behavior),
        "<class 'vobject.hcalendar.HCalendar'>"
    )
    cal.add('vevent')
    cal.vevent.add('summary').value = "this is a note"
    cal.vevent.add('url').value = "http://microformats.org/code/hcalendar/creator"
    cal.vevent.add('dtstart').value = datetime.date(2006,2,27)
    cal.vevent.add('location').value = "a place"
    cal.vevent.add('dtend').value = datetime.date(2006,2,27) + datetime.timedelta(days = 2)

    event2 = cal.add('vevent')
    event2.add('summary').value = "Another one"
    event2.add('description').value = "The greatest thing ever!"
    event2.add('dtstart').value = datetime.datetime(1998, 12, 17, 16, 42, tzinfo = tzs.get('US/Pacific'))
    event2.add('location').value = "somewhere else"
    event2.add('dtend').value = event2.dtstart.value + datetime.timedelta(days = 6)
    hcal = cal.serialize()
    """
    # self.assertEqual(
    #    str(hcal),
    #    """<span class="vevent">
    #           <a class="url" href="http://microformats.org/code/hcalendar/creator">
    #             <span class="summary">this is a note</span>:
    #              <abbr class="dtstart", title="20060227">Monday, February 27</abbr>
    #              - <abbr class="dtend", title="20060301">Tuesday, February 28</abbr>
    #              at <span class="location">a place</span>
    #           </a>
    #        </span>
    #        <span class="vevent">
    #           <span class="summary">Another one</span>:
    #           <abbr class="dtstart", title="19981217T164200-0800">Thursday, December 17, 16:42</abbr>
    #           - <abbr class="dtend", title="19981223T164200-0800">Wednesday, December 23, 16:42</abbr>
    #           at <span class="location">somewhere else</span>
    #           <div class="description">The greatest thing ever!</div>
    #        </span>
    #    """
    # )
