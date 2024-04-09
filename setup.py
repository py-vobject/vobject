"""
VObject: module for reading vCard and vCalendar files

Description
-----------

Parses iCalendar and vCard files into Python data structures, decoding the
relevant encodings. Also serializes vobject data structures to iCalendar, vCard,
or (experimentally) hCalendar unicode strings.

Requirements
------------

Requires python 2.7 or later, dateutil 2.4.0 or later and six.

Recent changes
--------------
    - Revert too-strict serialization of timestamp values - broke too many other
       implementations

For older changes, see
   - http://py-vobject.github.io/#release-history or
   - http://vobject.skyhouseconsulting.com/history.html
"""

from setuptools import setup, find_packages

doclines = (__doc__ or '').splitlines()

setup(zip_safe = True,
      include_package_data = True,
      install_requires=["python-dateutil >= 2.5.0; python_version < '3.10'",
                        "python-dateutil >= 2.7.0; python_version >= '3.10'",
                        "pytz", 'six'],
      platforms = ["any"],
      packages = find_packages(),
      long_description = "\n".join(doclines[2:]),
      test_suite="tests",
      )
