import io

import vobject

vcard_with_groups = (
    "home.begin:vcard\r\n"
    "version:3.0\r\n"
    "source:ldap://cn=Meister%20Berger,o=Universitaet%20Goerlitz,c=DE\r\n"
    "name:Meister Berger\r\n"
    "fn:Meister Berger\r\n"
    "n:Berger;Meister\r\n"
    "bday;value=date:1963-09-21\r\n"
    "o:Universitæt Görlitz\r\n"
    "title:Mayor\r\n"
    "title;language=de;value=text:Burgermeister\r\n"
    "note:The Mayor of the great city of\r\n"
    "  Goerlitz in the great country of Germany.\\nNext line.\r\n"
    "email;internet:mb@goerlitz.de\r\n"
    "home.tel;type=fax,voice;type=msg:+49 3581 123456\r\n"
    "home.label:Hufenshlagel 1234\\n\r\n"
    " 02828 Goerlitz\\n\r\n"
    " Deutschland\r\n"
    "END:VCARD\r\n"
)

simple_3_0_test = (
    "BEGIN:VCARD\r\n"
    "VERSION:3.0\r\n"
    "FN:Daffy Duck Knudson (with Bugs Bunny and Mr. Pluto)\r\n"
    "N:Knudson;Daffy Duck (with Bugs Bunny and Mr. Pluto)\r\n"
    "NICKNAME:gnat and gnu and pluto\r\n"
    "BDAY;value=date:02-10\r\n"
    "TEL;type=HOME:+01-(0)2-765.43.21\r\n"
    "TEL;type=CELL:+01-(0)5-555.55.55\r\n"
    "ACCOUNT;type=HOME:010-1234567-05\r\n"
    "ADR;type=HOME:;;Haight Street 512\\;\\nEscape\\, Test;Novosibirsk;;80214;Gnuland\r\n"
    "TEL;type=HOME:+01-(0)2-876.54.32\r\n"
    "ORG:University of Novosibirsk;Department of Octopus Parthenogenesis\r\n"
    "END:VCARD\r\n"
)

simple_4_0_test = (
    "BEGIN:VCARD\r\n"
    "VERSION:4.0\r\n"
    "UID:e47b1867-a0c6-4c09-b524-9a62b2bab208\r\n"
    "KIND:individual\r\n"
    "FN:Mr John Middle Smith, PhD\r\n"
    "N;ALTID=1;LANGUAGE=en:Smith;John;Middle;Mr;PhD\r\n"
    "N;ALTID=1;LANGUAGE=jp:春日;八郎;;;\r\n"
    "GENDER:M;male\r\n"
    "LANG;TYPE=work;PREF=1:en\r\n"
    "LANG;TYPE=work;PREF=2:fr\r\n"
    "ORG:Some Company\r\n"
    "TEL;TYPE=cell;PID=3.1,4.2;VALUE=uri:tel:+1-111-555-1236\r\n"
    'TEL;TYPE="home,video":+1 222-555-4654\r\n'
    "EMAIL;TYPE=home;PID=4.1,5.2:home@myemail.com\r\n"
    "EMAIL;TYPE=work:work@myemail.com\r\n"
    'ADR;TYPE=home;LABEL="55 My Street\\nSpringfield , Some County 55555\\nUS":;;5\r\n'
    " 5 My Street;Springfield ;Some County;55555;US\r\n"
    'ADR;TYPE=work;LABEL="66 Another Street\\nAnother City, A County 66666\\nUS":;\r\n'
    " ;66 Another Street;Another City;A County;66666;US\r\n"
    "NOTE:Notes about the contact\r\n"
    "URL:http://www.mywebsite.com\r\n"
    "FBURL;MEDIATYPE=text/calendar:ftp://example.com/busy/project-a.ifb\r\n"
    "CALADRURI:http://example.com/calendar/jdoe\r\n"
    "CALURI;MEDIATYPE=text/calendar:ftp://ftp.example.com/calA.ics\r\n"
    "IMPP;PREF=1:xmpp:alice@example.com\r\n"
    "BDAY:20000430\r\n"
    "ANNIVERSARY:20240430\r\n"
    "RELATED;TYPE=co-worker;VALUE=text:Related Person\r\n"
    "RELATED;TYPE=friend;VALUE=text:Another Related Person\r\n"
    "CLIENTPIDMAP:1;urn:uuid:3df403f4-5924-4bb7-b077-3c711d9eb34b\r\n"
    "CLIENTPIDMAP:2;urn:uuid:d89c9c7a-2e1b-4832-82de-7e992d95faa5\r\n"
    "REV:20240430T205447Z\r\n"
    "END:VCARD\r\n"
)


def test_vcard_creation():
    """
    Test creating a vCard
    """
    vcard = vobject.base.newFromBehavior("vcard", "3.0")
    assert str(vcard) == "<VCARD| []>"


def test_default_behavior():
    """
    Default behavior test.
    """
    card = vobject.readOne(io.StringIO(vcard_with_groups))
    assert vobject.base.getBehavior("note") is None
    assert (
        str(card.note.value) == "The Mayor of the great city of Goerlitz in the great country of Germany.\nNext line."
    )


def test_with_groups():
    """
    vCard groups test
    """
    card = vobject.readOne(io.StringIO(vcard_with_groups))
    assert str(card.group) == "home"
    assert str(card.tel.group) == "home"

    card.group = card.tel.group = "new"
    assert str(card.tel.serialize().strip()) == "new.TEL;TYPE=fax,voice,msg:+49 3581 123456"
    assert str(card.serialize().splitlines()[0]) == "new.BEGIN:VCARD"


def test_vcard_3_parsing():
    """
    VCARD 3.0 parse test
    """
    card = vobject.base.readOne(io.StringIO(simple_3_0_test))
    # value not rendering correctly?
    # self.assertEqual(
    #    card.adr.value,
    #    "<Address: Haight Street 512;\nEscape, Test\nNovosibirsk,  80214\nGnuland>"
    # )
    assert card.org.value == ["University of Novosibirsk", "Department of Octopus Parthenogenesis"]

    for _ in range(3):
        new_card = vobject.base.readOne(card.serialize())
        assert new_card.org.value == card.org.value
        card = new_card


def test_vcard_4_parsing():
    """
    VCARD 4.0 parse test
    """
    card = vobject.base.readOne(io.StringIO(simple_4_0_test))

    for _ in range(3):
        new_card = vobject.base.readOne(card.serialize())
        assert new_card.org.value == card.org.value
        assert new_card.clientpidmap.value == card.clientpidmap.value
        assert new_card.gender.value == card.gender.value
        card = new_card
