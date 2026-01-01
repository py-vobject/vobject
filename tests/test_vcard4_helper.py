"""Test the vCard4() helper function"""

import vobject


def test_vcard4_helper():
    """Test that vCard4() creates a vCard 4.0 object"""
    # Create a vCard 4.0 using the helper
    v = vobject.vCard4()

    # Add some content
    v.add('fn').value = 'Test Person'
    v.add('n')
    v.n.value = vobject.vcard.Name(family='Person', given='Test')

    # Add vCard 4.0 specific properties
    v.add('kind').value = 'individual'
    v.add('gender').value = 'M'

    # Serialize (this will auto-generate VERSION if not present)
    result = v.serialize()

    # Verify it's vCard 4.0
    assert 'VERSION:4.0' in result, "VERSION:4.0 not found in output"
    assert 'KIND:individual' in result, "KIND property not found"
    assert 'GENDER:M' in result, "GENDER property not found"
    assert 'FN:Test Person' in result, "FN property not found"
    assert 'N:Person;Test;;;' in result, "N property not found"

    # Check the version after serialization
    assert v.version.value == '4.0', f"Expected version 4.0, got {v.version.value}"


def test_vcard4_default_version():
    """Test that vCard4() auto-generates VERSION:4.0 on serialization"""
    v = vobject.vCard4()
    v.add('fn').value = 'Test'

    # VERSION is auto-generated during serialization
    serialized = v.serialize()

    assert 'VERSION:4.0' in serialized, "VERSION:4.0 not found in serialized output"
    assert hasattr(v, 'version'), "VERSION property not found after serialization"
    assert v.version.value == '4.0', f"Expected version 4.0, got {v.version.value}"


def test_vcard_vs_vcard4_comparison():
    """Compare vCard() vs vCard4() helper functions"""
    # vCard 3.0
    v3 = vobject.vCard()
    v3.add('fn').value = 'John Doe'
    serialized_v3 = v3.serialize()

    assert 'VERSION:3.0' in serialized_v3, "vCard() should create vCard 3.0"
    assert v3.version.value == '3.0', f"Expected version 3.0, got {v3.version.value}"

    # vCard 4.0
    v4 = vobject.vCard4()
    v4.add('fn').value = 'John Doe'
    serialized_v4 = v4.serialize()

    assert 'VERSION:4.0' in serialized_v4, "vCard4() should create vCard 4.0"
    assert v4.version.value == '4.0', f"Expected version 4.0, got {v4.version.value}"


def test_vcard4_with_multiple_properties():
    """Test vCard4() with multiple vCard 4.0 specific properties"""
    v = vobject.vCard4()

    # Add required properties
    v.add('fn').value = 'Jane Smith'
    v.add('n')
    v.n.value = vobject.vcard.Name(family='Smith', given='Jane')

    # Add vCard 4.0 specific properties
    v.add('kind').value = 'individual'
    v.add('gender').value = 'F'
    v.add('anniversary').value = '20150714'

    lang = v.add('lang')
    lang.value = 'en-US'
    lang.params['PREF'] = ['1']

    impp = v.add('impp')
    impp.value = 'xmpp:jane@example.com'

    serialized = v.serialize()

    # Verify all properties are present
    assert 'VERSION:4.0' in serialized
    assert 'FN:Jane Smith' in serialized
    assert 'N:Smith;Jane;;;' in serialized
    assert 'KIND:individual' in serialized
    assert 'GENDER:F' in serialized
    assert 'ANNIVERSARY:20150714' in serialized
    assert 'LANG;PREF=1:en-US' in serialized
    assert 'IMPP:xmpp:jane@example.com' in serialized
