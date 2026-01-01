"""Test vCard 4.0 implementation"""

import vobject


def test_basic_vcard40():
    """Test creating a basic vCard 4.0"""
    # Create a new vCard 4.0
    v = vobject.vCard()
    v.behavior = vobject.vcard40.VCard4_0
    v.add('fn').value = 'John Doe'
    v.add('n')
    v.n.value = vobject.vcard.Name(family='Doe', given='John')

    # Add vCard 4.0 VERSION
    if hasattr(v, 'version'):
        del v.version
    v.add('version').value = '4.0'

    serialized = v.serialize()

    assert 'BEGIN:VCARD' in serialized
    assert 'VERSION:4.0' in serialized
    assert 'FN:John Doe' in serialized
    assert 'N:Doe;John;;;' in serialized
    assert 'END:VCARD' in serialized


def test_new_properties():
    """Test vCard 4.0 new properties"""
    v = vobject.vCard()
    v.behavior = vobject.vcard40.VCard4_0

    # Required properties
    v.add('fn').value = 'Jane Smith'
    v.add('version').value = '4.0'

    # New KIND property
    v.add('kind').value = 'individual'

    # New GENDER property
    v.add('gender').value = 'F'

    # New ANNIVERSARY property
    v.add('anniversary').value = '20100615'

    # New LANG property
    lang = v.add('lang')
    lang.value = 'en'
    lang.params['PREF'] = ['1']

    # New IMPP property
    impp = v.add('impp')
    impp.value = 'xmpp:jane@example.com'

    # New RELATED property
    related = v.add('related')
    related.value = 'http://example.com/directory/jsmith.vcf'
    related.params['TYPE'] = ['spouse']

    # New SOURCE property
    v.add('source').value = 'http://example.com/directory/jsmith.vcf'

    serialized = v.serialize()

    assert 'FN:Jane Smith' in serialized
    assert 'VERSION:4.0' in serialized
    assert 'KIND:individual' in serialized
    assert 'GENDER:F' in serialized
    assert 'ANNIVERSARY:20100615' in serialized
    assert 'LANG;PREF=1:en' in serialized
    assert 'IMPP:xmpp:jane@example.com' in serialized
    assert 'RELATED;TYPE=spouse:http://example.com/directory/jsmith.vcf' in serialized
    assert 'SOURCE:http://example.com/directory/jsmith.vcf' in serialized


def test_modified_properties():
    """Test modified properties in vCard 4.0"""
    v = vobject.vCard()
    v.behavior = vobject.vcard40.VCard4_0

    # Required properties
    v.add('fn').value = 'Bob Johnson'
    v.add('version').value = '4.0'

    # PHOTO as URI (vCard 4.0 style)
    v.add('photo').value = 'http://example.com/photo.jpg'

    # TEL with URI scheme
    tel = v.add('tel')
    tel.value = 'tel:+1-555-555-5555'
    tel.params['TYPE'] = ['voice', 'home']
    tel.params['PREF'] = ['1']

    # GEO as geo: URI
    v.add('geo').value = 'geo:37.386013,-122.082932'

    # UID as URN
    v.add('uid').value = 'urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6'

    serialized = v.serialize()

    assert 'FN:Bob Johnson' in serialized
    assert 'VERSION:4.0' in serialized
    assert 'PHOTO:http://example.com/photo.jpg' in serialized
    assert 'TEL;PREF=1;TYPE=voice,home:tel:+1-555-555-5555' in serialized or \
           'TEL;TYPE=voice,home;PREF=1:tel:+1-555-555-5555' in serialized
    assert 'GEO:geo:37.386013,-122.082932' in serialized
    assert 'UID:urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6' in serialized


def test_group_vcard():
    """Test vCard 4.0 group with MEMBER property"""
    v = vobject.vCard()
    v.behavior = vobject.vcard40.VCard4_0

    # Required properties
    v.add('fn').value = 'Development Team'
    v.add('version').value = '4.0'

    # KIND=group
    v.add('kind').value = 'group'

    # MEMBER properties (only valid for groups)
    v.add('member').value = 'urn:uuid:03a0e51f-d1aa-4385-8a53-e29025acd8af'
    v.add('member').value = 'urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6'
    v.add('member').value = 'mailto:member1@example.com'

    serialized = v.serialize()

    assert 'FN:Development Team' in serialized
    assert 'VERSION:4.0' in serialized
    assert 'KIND:group' in serialized
    assert 'MEMBER:urn:uuid:03a0e51f-d1aa-4385-8a53-e29025acd8af' in serialized
    assert 'MEMBER:urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6' in serialized
    assert 'MEMBER:mailto:member1@example.com' in serialized


def test_multiple_fn():
    """Test multiple FN values (allowed in vCard 4.0)"""
    v = vobject.vCard()
    v.behavior = vobject.vcard40.VCard4_0

    # Multiple FN values with different languages
    v.add('version').value = '4.0'

    fn1 = v.add('fn')
    fn1.value = 'John Doe'
    fn1.params['LANGUAGE'] = ['en']

    fn2 = v.add('fn')
    fn2.value = 'ジョン・ドゥ'
    fn2.params['LANGUAGE'] = ['ja']

    serialized = v.serialize()

    assert 'VERSION:4.0' in serialized
    assert 'FN;LANGUAGE=en:John Doe' in serialized
    assert 'FN;LANGUAGE=ja:ジョン・ドゥ' in serialized

    # Verify we have exactly 2 FN lines
    fn_count = serialized.count('\nFN')
    assert fn_count == 2, f"Expected 2 FN properties, found {fn_count}"


def test_new_parameters():
    """Test new vCard 4.0 parameters"""
    v = vobject.vCard()
    v.behavior = vobject.vcard40.VCard4_0

    v.add('version').value = '4.0'
    v.add('fn').value = 'Alice Williams'

    # PREF parameter (replaces TYPE=pref)
    tel1 = v.add('tel')
    tel1.value = 'tel:+1-555-111-1111'
    tel1.params['PREF'] = ['1']
    tel1.params['TYPE'] = ['work']

    tel2 = v.add('tel')
    tel2.value = 'tel:+1-555-222-2222'
    tel2.params['PREF'] = ['2']
    tel2.params['TYPE'] = ['home']

    # ALTID parameter (links alternate representations)
    email1 = v.add('email')
    email1.value = 'alice@work.example.com'
    email1.params['ALTID'] = ['1']

    email2 = v.add('email')
    email2.value = 'alice.williams@work.example.com'
    email2.params['ALTID'] = ['1']

    # MEDIATYPE parameter
    photo = v.add('photo')
    photo.value = 'http://example.com/photo.jpg'
    photo.params['MEDIATYPE'] = ['image/jpeg']

    serialized = v.serialize()

    assert 'FN:Alice Williams' in serialized
    assert 'VERSION:4.0' in serialized

    # Check PREF parameter on TEL
    assert 'PREF=1' in serialized
    assert 'PREF=2' in serialized
    assert 'tel:+1-555-111-1111' in serialized
    assert 'tel:+1-555-222-2222' in serialized

    # Check ALTID parameter on EMAIL
    assert 'EMAIL;ALTID=1:alice@work.example.com' in serialized or \
           'EMAIL;ALTID=1:alice.williams@work.example.com' in serialized
    assert serialized.count('ALTID=1') == 2, "Expected 2 EMAIL properties with ALTID=1"

    # Check MEDIATYPE parameter on PHOTO
    assert 'PHOTO;MEDIATYPE=image/jpeg:http://example.com/photo.jpg' in serialized
