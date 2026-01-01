"""Definitions and behavior for vCard 4.0"""

import codecs

from . import behavior

from .base import ContentLine, registerBehavior, backslashEscape, str_
from .icalendar import stringToTextValues
from .vcard import (
    VCardBehavior,
    VCardTextBehavior,
    Name,
    NameBehavior,
    Address,
    AddressBehavior,
    OrgBehavior,
    toListOrString,
    splitFields,
    toList,
    serializeFields,
    NAME_ORDER,
    ADDRESS_ORDER,
    REALLY_LARGE,
    wacky_apple_photo_serialize
)


# Python 3 no longer has a basestring type, so....
try:
    basestring = basestring
except NameError:
    basestring = (str, bytes)


# ------------------------ vCard 4.0 Main Component ----------------------------

class VCard4_0(VCardBehavior):
    """
    vCard 4.0 behavior.
    """
    name = 'VCARD'
    description = 'vCard 4.0, defined in RFC 6350'
    versionString = '4.0'
    isComponent = True
    sortFirst = ('version', 'prodid', 'uid')
    knownChildren = {
        'VERSION':      (1, 1, None),     # exactly one, required
        'FN':           (1, None, None),  # one or more, required
        'N':            (0, 1, None),     # at most one
        'NICKNAME':     (0, None, None),
        'PHOTO':        (0, None, None),
        'BDAY':         (0, 1, None),
        'ANNIVERSARY':  (0, 1, None),     # new in 4.0
        'GENDER':       (0, 1, None),     # new in 4.0
        'ADR':          (0, None, None),
        'TEL':          (0, None, None),
        'EMAIL':        (0, None, None),
        'IMPP':         (0, None, None),  # new in 4.0
        'LANG':         (0, None, None),  # new in 4.0
        'TZ':           (0, None, None),
        'GEO':          (0, None, None),
        'TITLE':        (0, None, None),
        'ROLE':         (0, None, None),
        'LOGO':         (0, None, None),
        'ORG':          (0, None, None),
        'MEMBER':       (0, None, None),  # new in 4.0, only for KIND=group
        'RELATED':      (0, None, None),  # new in 4.0
        'CATEGORIES':   (0, None, None),
        'NOTE':         (0, None, None),
        'PRODID':       (0, 1, None),
        'REV':          (0, 1, None),
        'SORT-STRING':  (0, None, None),  # deprecated in 4.0, but may exist
        'SOUND':        (0, None, None),
        'UID':          (0, 1, None),
        'CLIENTPIDMAP': (0, None, None),  # new in 4.0
        'URL':          (0, None, None),
        'VERSION':      (1, 1, None),
        'KEY':          (0, None, None),
        'FBURL':        (0, None, None),
        'CALADRURI':    (0, None, None),
        'CALURI':       (0, None, None),
        'XML':          (0, None, None),  # new in 4.0
        'SOURCE':       (0, None, None),  # new in 4.0
        'KIND':         (0, 1, None),     # new in 4.0
    }

    @classmethod
    def generateImplicitParameters(cls, obj):
        """
        Create VERSION if needed.

        For vCard 4.0, VERSION must be immediately after BEGIN:VCARD.
        """
        if not hasattr(obj, 'version'):
            obj.add(ContentLine('VERSION', [], cls.versionString))


registerBehavior(VCard4_0)


# ------------------------ vCard 4.0 New Properties ----------------------------

class Kind(VCardTextBehavior):
    """
    KIND property for vCard 4.0.

    Valid values: individual, group, org, location, or x-name/iana-token
    Default (if not present): individual
    """
    name = "KIND"
    description = 'Kind of object (individual, group, org, location)'


registerBehavior(Kind)


class Gender(VCardTextBehavior):
    """
    GENDER property for vCard 4.0.

    Format: sex-component;text-component
    sex-component: M, F, O, N, U, or empty
    text-component: free-form text (optional)

    Examples:
        GENDER:M
        GENDER:F;female
        GENDER:O;intersex
        GENDER:;it's complicated
    """
    name = "GENDER"
    description = 'Sex and gender identity'

    @classmethod
    def decode(cls, line):
        """Decode the gender value."""
        if line.encoded:
            # Gender is semicolon-separated: sex;text
            line.value = stringToTextValues(line.value)[0]
            line.encoded = False


registerBehavior(Gender)


class Anniversary(VCardTextBehavior):
    """
    ANNIVERSARY property for vCard 4.0.

    Date of marriage or anniversary. Can be date, date-time, or partial date.
    Examples:
        ANNIVERSARY:19960415
        ANNIVERSARY:--0415
    """
    name = "ANNIVERSARY"
    description = 'Date of marriage or equivalent'


registerBehavior(Anniversary)


class Lang(VCardTextBehavior):
    """
    LANG property for vCard 4.0.

    Language tag (RFC 5646) for language preferences.
    Can have PREF parameter for ordering.

    Examples:
        LANG;PREF=1:en
        LANG;PREF=2:fr
    """
    name = "LANG"
    description = 'Language preference'


registerBehavior(Lang)


class Impp(VCardTextBehavior):
    """
    IMPP property for vCard 4.0.

    Instant messaging and presence protocol URI.

    Examples:
        IMPP;PREF=1:xmpp:alice@example.com
        IMPP:sip:alice@example.com
        IMPP:skype:alice.example
    """
    name = "IMPP"
    description = 'Instant messaging and presence protocol URI'


registerBehavior(Impp)


class Related(VCardTextBehavior):
    """
    RELATED property for vCard 4.0.

    Relationship to another entity. Can be URI or text.
    TYPE parameter specifies relationship type.

    Examples:
        RELATED;TYPE=friend:urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6
        RELATED;TYPE=co-worker;VALUE=text:Jane Doe
        RELATED;TYPE=spouse:http://example.com/directory/jdoe.vcf
    """
    name = "RELATED"
    description = 'Relationship to another entity'


registerBehavior(Related)


class Member(VCardTextBehavior):
    """
    MEMBER property for vCard 4.0.

    Only valid when KIND=group. Defines members of the group.
    Value is a URI (often urn:uuid:).

    Examples:
        MEMBER:urn:uuid:03a0e51f-d1aa-4385-8a53-e29025acd8af
        MEMBER:mailto:subscriber1@example.com
    """
    name = "MEMBER"
    description = 'Group member (only for KIND=group)'


registerBehavior(Member)


class ClientPidMap(VCardTextBehavior):
    """
    CLIENTPIDMAP property for vCard 4.0.

    Maps PID values to URIs for synchronization.
    Format: integer;URI

    Examples:
        CLIENTPIDMAP:1;urn:uuid:3df403f4-5924-4bb7-b077-3c711d9eb34b
    """
    name = "CLIENTPIDMAP"
    description = 'Client PID mapping for synchronization'


registerBehavior(ClientPidMap)


class Xml(VCardTextBehavior):
    """
    XML property for vCard 4.0.

    Extended XML-encoded vCard data.
    Must have VALUE=text parameter (default).

    Example:
        XML:<ext xmlns="http://example.com/ext">data</ext>
    """
    name = "XML"
    description = 'Extended XML-encoded vCard data'


registerBehavior(Xml)


class Source(VCardTextBehavior):
    """
    SOURCE property for vCard 4.0.

    URI for the source of the vCard data.

    Examples:
        SOURCE:http://example.com/directory/jdoe.vcf
        SOURCE:ldap://ldap.example.com/cn=John%20Doe,o=Example%20Corp,c=US
    """
    name = "SOURCE"
    description = 'Source URI for directory information'


registerBehavior(Source)


# ------------------------ Modified Properties for vCard 4.0 -------------------

class Photo4_0(VCardTextBehavior):
    """
    PHOTO property for vCard 4.0.

    In vCard 4.0, PHOTO is a URI value (can use data: URI for inline).
    Binary encoding via BASE64 parameter is deprecated.

    Examples:
        PHOTO:http://example.com/photo.jpg
        PHOTO;MEDIATYPE=image/jpeg:data:image/jpeg;base64,MIICajCCA...
    """
    name = "Photo"
    description = 'Photograph (URI or data URI in vCard 4.0)'

    @classmethod
    def valueRepr(cls, line):
        return " (PHOTO URI at 0x{0!s}) ".format(id(line.value))

    @classmethod
    def serialize(cls, obj, buf, lineLength, validate):
        """
        Apple's Address Book compatibility for images.
        """
        if wacky_apple_photo_serialize:
            lineLength = REALLY_LARGE
        VCardTextBehavior.serialize(obj, buf, lineLength, validate)


registerBehavior(Photo4_0, 'PHOTO', id_='4.0')


class Logo4_0(VCardTextBehavior):
    """
    LOGO property for vCard 4.0.

    In vCard 4.0, LOGO is a URI value (can use data: URI for inline).

    Examples:
        LOGO:http://example.com/logo.png
        LOGO;MEDIATYPE=image/png:data:image/png;base64,iVBORw0KG...
    """
    name = "Logo"
    description = 'Logo (URI or data URI in vCard 4.0)'

    @classmethod
    def valueRepr(cls, line):
        return " (LOGO URI at 0x{0!s}) ".format(id(line.value))

    @classmethod
    def serialize(cls, obj, buf, lineLength, validate):
        """
        Handle logo serialization similarly to photos.
        """
        if wacky_apple_photo_serialize:
            lineLength = REALLY_LARGE
        VCardTextBehavior.serialize(obj, buf, lineLength, validate)


registerBehavior(Logo4_0, 'LOGO', id_='4.0')


class Sound4_0(VCardTextBehavior):
    """
    SOUND property for vCard 4.0.

    In vCard 4.0, SOUND is a URI value (can use data: URI for inline).

    Examples:
        SOUND:http://example.com/sound.ogg
        SOUND;MEDIATYPE=audio/ogg:data:audio/ogg;base64,T2dnUw...
    """
    name = "Sound"
    description = 'Sound (URI or data URI in vCard 4.0)'

    @classmethod
    def valueRepr(cls, line):
        return " (SOUND URI at 0x{0!s}) ".format(id(line.value))


registerBehavior(Sound4_0, 'SOUND', id_='4.0')


class Geo4_0(VCardTextBehavior):
    """
    GEO property for vCard 4.0.

    In vCard 4.0, GEO is a URI using the geo: scheme (RFC 5870).
    In vCard 3.0, it was semicolon-separated lat;long values.

    Examples:
        GEO:geo:37.386013,-122.082932
        GEO:geo:48.198634,16.371648;crs=wgs84;u=40
    """
    name = "Geo"
    description = 'Geographic position (geo: URI in vCard 4.0)'


registerBehavior(Geo4_0, 'GEO', id_='4.0')


class Key4_0(VCardTextBehavior):
    """
    KEY property for vCard 4.0.

    In vCard 4.0, KEY can be URI or text.
    Can use data: URI for inline key data.

    Examples:
        KEY:http://example.com/key.pgp
        KEY;MEDIATYPE=application/pgp-keys:data:application/pgp-keys;base64,LS0t...
        KEY:data:application/pgp-keys;base64,LS0t...
    """
    name = "Key"
    description = 'Public key or authentication certificate (URI or text in vCard 4.0)'


registerBehavior(Key4_0, 'KEY', id_='4.0')


class Tel4_0(VCardTextBehavior):
    """
    TEL property for vCard 4.0.

    In vCard 4.0, TEL should use VALUE=uri with tel: scheme.
    For backward compatibility, text values are still supported.

    TYPE parameter values changed:
    - Old: HOME, WORK, VOICE, FAX, CELL, etc.
    - New: text, voice, fax, cell, video, pager, textphone

    Examples:
        TEL;VALUE=uri;PREF=1;TYPE="voice,home":tel:+1-555-555-5555
        TEL;TYPE=cell:tel:+1-555-123-4567
        TEL;VALUE=text:+1-555-555-5555
    """
    name = "Tel"
    description = 'Telephone number (preferably tel: URI in vCard 4.0)'


registerBehavior(Tel4_0, 'TEL', id_='4.0')


class Uid4_0(VCardTextBehavior):
    """
    UID property for vCard 4.0.

    In vCard 4.0, UID is preferably a URI (often urn:uuid:).
    Plain text UIDs are still supported for backward compatibility.

    Examples:
        UID:urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6
        UID:http://example.com/contacts/jdoe
    """
    name = "Uid"
    description = 'Unique identifier (preferably URI in vCard 4.0)'


registerBehavior(Uid4_0, 'UID', id_='4.0')


# ------------------------ vCard 4.0 FN with updated cardinality ----------------

class FN4_0(VCardTextBehavior):
    """
    FN property for vCard 4.0.

    In vCard 4.0, FN has cardinality 1* (one or more required).
    This allows multiple formatted names for different contexts.

    Examples:
        FN:John Doe
        FN;LANGUAGE=en:John Doe
        FN;LANGUAGE=jp:ジョン・ドゥ
    """
    name = "FN"
    description = 'Formatted name (one or more required in vCard 4.0)'


registerBehavior(FN4_0, 'FN', id_='4.0')
