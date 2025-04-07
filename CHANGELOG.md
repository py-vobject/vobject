Python vObject Release Notes
============================

vobject 0.9.9 released
--
16 December 2024

To install, use `pip install vobject`, or download the archive and
untar, run `python setup.py install`. Tests can be run via `python
setup.py test`.
_dateutil_ and _six_ are required.
Python 2.7 or higher is required.

* Added product version to PRODID tag in iCalendar headers
* Added support for GEO tags in vCards

vobject 0.9.8 released
--
2 October 2024

To install, use `pip install vobject`, or download the archive and
untar, run `python setup.py install`. Tests can be run via `python
setup.py test`.
_dateutil_ and _six_ are required.
Python 2.7 or higher is required.

* Accumulated bug fixes

vobject 0.9.7 released
--
24 February 2024

To install, use `pip install vobject`, or download the archive and
untar, run `python setup.py install`. Tests can be run via `python
setup.py test`.
_dateutil_ and _six_ are required.
Python 2.7 or higher is required.

* New repository: https://github.com/py-vobject/vobject
* New website: https://py-object.github.io
* New maintainers
* Cosmetic release, switching to new maintenance organization.
  * This release is functionally identical to 0.9.6.1.

vobject 0.9.6 released
--
7 July 2018

To install, use `pip install vobject`, or download the archive and
untar, run `python setup.py install`. Tests can be run via `python
setup.py test`.
_dateutil_ and _six_ are required.
Python 2.7 or higher is required.

* Correctly order calendar properties before calendar components
* Correctly serialize timestamp values (i.e. `REV`)
* Pass correct formatting string to logger
* RRULE: Fix floating UNTIL with dateutil > 2.6.1
* Encode params if necessary in serialization
* Ignore escaped semi-colons in UNTIL value
* RRULE: Fix VTODO without DTSTART
* Fixed regexp for VCF Version 2.1
* repr() changed for datetime.timedelta in python 3.7

vobject 0.9.5 released
--
29 June 2017

To install, use `pip install vobject`, or download the archive and
untar, run `python setup.py install`. Tests can be run via `python
setup.py test`.
_dateutil_ and _six_ are required.
Python 2.7 or higher is required.

* Make `ics_diff.py` work with Python 3
* Huge changes to text encoding for Python 2/3 compatibility
* Autogenerate DTSTAMP if not provided
* Fix `getrruleset()` for Python 3 and in the case that `addRDate=True`
* Update vCard property validation to match specifications
* Handle offset-naive and offset-aware datetimes in recurrence rules
* Improved documentation for multi-value properties

vobject 0.9.4.1 released
--
22 January 2017

To install, use `pip install vobject`, or download the archive and
untar, run `python setup.py install`. Tests can be run via `python
setup.py test`.
_dateutil_ and _six_ are required.
Python 2.7 or higher is required.

* Pickling/deepcopy hotfix

vobject 0.9.4 released
--
20 January 2017

To install, use `pip install vobject`, or download the archive and
untar, run `python setup.py install`. Tests can be run via `python
setup.py test`.
_dateutil_ and _six_ are required.
Python 2.7 or higher is required.

* Improved PEP8 compliance
* Improved Python 3 compatibility
* Improved encoding/decoding
* Correct handling of _pytz_ timezones

vobject 0.9.3 released
--
26 August 2016

To install, use `pip install vobject`, or download the archive and
untar, run `python setup.py install`. Tests can be run via `python
setup.py test`.
_dateutil_ and _six_ are required.
Python 2.7 or higher is required.

* Fixed use of doc in `setup.py` for -OO mode
* Added python3 compatibility for base64 encoding
* Fixed ORG fields with multiple components
* Handle _pytz_ timezones in iCalendar serialization
* Use logging instead of printing to stdout

vobject 0.9.2 released
--
13 March 2016

To install, use `pip install vobject`, or download the archive and
untar, run `python setup.py install`. Tests can be run via `python
setup.py test`.
_dateutil_ and _six_ are required.
Python 2.7 or higher is required.

* Better line folding for UTF-8 strings
* Convert unicode to UTF-8 to be _StringIO_ compatible

vobject 0.9.1 released
--
16 February 2016

To install, use `pip install vobject`, or download the archive and
untar, run `python setup.py install`. Tests can be run via `python
setup.py test`.
_dateutil_ and _six_ are required.
Python 2.7 or higher is now required.

* Removed lock on _dateutil_ version (>=2.4.0 now works)

vobject 0.9.0 released
--
3 February 2016

To install, use `pip install vobject`, or download the archive and
untar, run `python setup.py install`. Tests can be run via `python
setup.py test`.
_dateutil 2.4.0_ and _six_ are required.
Python 2.7 or higher is now required.

* Python 3 compatible
* Requires Python 2.7 or later (was Python 2.4)
* New dependency on _six_ for Python 2/Python 3 compatibility
* Updated version of _dateutil_ (2.4.0)
* More comprehensive unit tests available in `tests.py`
* Performance improvements in iteration
* Test files are included in PyPI download package

vobject 0.8.2 released
--
28 January 2016

To install, use `pip install vobject`, or download the archive and
untar, run `python setup.py install`. Tests can be run via `python
setup.py test`.
_dateutil 1.1_ or later is required.
Python 2.4 is also required.

* Removed unnecessary `ez_setup` call from `setup.py`
* Moved source code repository to GitHub
* New maintainer Sameen Karim

vobject 0.8.1c released (SVN revision 217)
--
27 February 2009

To install, use _easy_install_, or download the archive and untar, run
`python setup.py install`. Tests can be run via `python setup.py test`.
_dateutil 1.1_ or later is required.
Python 2.4 or later is required.

* Tweaked `change_tz.py` to keep it 2.4 compatible

vobject 0.8.1b released (SVN revision 216)
--
12 January 2009

To install, use _easy_install_, or download the archive and untar, run
`python setup.py install`. Tests can be run via `python setup.py test`.
_dateutil 1.1_ or later is required.
Python 2.4 is also required.

* Change behavior when import a VCALENDAR or VCARD with an older or
  absent VERSION line, now the most recent behavior (i.e., VCARD 3.0
  and iCalendar, VCALENDAR 2.0) is used

vobject 0.8.0 released (SVN revision 213)
--
29 December 2008

To install, use _easy_install_, or download the archive and untar, run
`python setup.py install`. Tests can be run via `python setup.py test`.
_dateutil 1.1_ or later is required.
Python 2.4 is also required.

* Changed license to Apache 2.0 from Apache 1.1
* Fixed a major performance bug in backslash decoding large text bodies
* Added workaround for strange Apple Address Book parsing of vcard PHOTO,
  don't wrap PHOTO by default. To disable this behavior, set
  `vobject.vcard.wacky_apple_photo_serialize` to `False`.

vobject 0.7.1 released (SVN revision 208)
--
25 July 2008

To install, use _easy_install_, or download the archive and untar, run
`python setup.py install`. Tests can be run via `python setup.py test`.
`_dateutil 1.1_` or later is required. Python 2.4 is also required.

* Add `change_tz` script for converting timezones in iCalendar files

vobject 0.7.0 released (SVN revision 206)
--
16 July 2008

To install, use _easy_install_, or download the archive and untar, run
`python setup.py install`. Tests can be run via `python setup.py test`.
_dateutil 1.1_ or later is required.
Python 2.4 is also required.

* Allow Outlook's technically illegal use of commas in TZIDs
* Added introspection help for IPython so tab completion works with
  vobject's custom __getattr__
* Made vobjects pickle-able
* Added tolerance for the escaped semi-colons in RRULEs a Ruby iCalendar
  library generates
* Fixed Bug 12245, setting an rrule from a dateutil instance missed
  BYMONTHDAY when the number used is negative

vobject 0.6.6 released (SVN revision 201)
--
30 May 2008

To install, use _easy_install_, or download the archive and untar, run
`python setup.py install`. Tests can be run via `python setup.py test`.
_dateutil 1.1_ or later is required.
Python 2.4 is also required.

* Fixed bug 12120, unicode TZIDs were failing to parse.

vobject 0.6.5 released (SVN revision 200)
--
28 May 2008

To install, use _easy_install_, or download the archive and untar, run
`python setup.py install`. Tests can be run via `python setup.py test`.
_dateutil 1.1_ or later is required.
Python 2.4 is also required.

* Fixed bug 9814, quoted-printable data wasn't being decoded into unicode,
  thanks to Ilpo NyyssÃ¶nen for the fix.
* Fixed bug 12008, silently translate buggy Lotus Notes names with
  underscores into dashes.

vobject 0.6.0 released (SVN revision 193)
--
21 February 2008

To install, use _easy_install_, or download the archive and untar, run
`python setup.py install`.
_dateutil 1.1_ or later is required.
Python 2.4 is also required.

* Added VAVAILABILITY support, thanks to the Calendar Server team.
* Improved unicode line folding.

vobject 0.5.0 released (SVN revision 189)
--
14 January 2008

To install, use _easy_install_, or download the archive and untar, run
`python setup.py install`.
_dateutil 1.1_ or later is required.
Python 2.4 is also required.

* Updated to more recent `ez_setup`, vobject wasn't successfully installing.

vobject 0.4.9 released (SVN revision 187)
--
19 November 2007

To install, use _easy_install_, or download the archive and untar, run
`python setup.py install`.
_dateutil 1.1_ or later is required.
Python 2.4 is also required.

* Tolerate invalid UNTIL values for recurring events
* Minor improvements to logging and tracebacks
* Fix serialization of zero-delta durations
* Treat different tzinfo classes that represent UTC as equal
* Added ORG behavior to vCard handling, native value for ORG is now a list.

vobject 0.4.8 released (SVN revision 180)
--
7 January 2007

To install, use _easy_install_, or download the archive and untar, run
`python setup.py install`.
_dateutil 1.1_ or later is required.
Python 2.4 is also required.

* Fixed problem with the UNTIL time used when creating a dateutil rruleset.

vobject 0.4.7 released (SVN revision 172), hot on the heals of yesterday's 0.4.6
--
21 December 2006

To install, use _easy_install_, or download the archive and untar, run
`python setup.py install`.
_dateutil 1.1_ or later is required.
Python 2.4 is also required.

* Fixed a problem causing DATE valued RDATEs and EXDATEs to be ignored
  when interpreting recurrence rules
* And, from the short lived vobject 0.4.6, added an `ics_diff` module
  and an `ics_diff` command line script for comparing similar iCalendar
  files

vobject 0.4.6 released (SVN revision 171)
--
20 December 2006

To install, use _easy_install_, or download the archive and untar, run
`python setup.py install`.
_dateutil 1.1_ or later is required.
Python 2.4 is also required.

* Added an ics_diff module and an ics_diff command line script for
  comparing similar iCalendar files

vobject 0.4.5 released (SVN revision 168)
--
8 December 2006

To install, use _easy_install_, or download the archive and untar, run
`python setup.py install`.
_dateutil 1.1_ or later is required.
Python 2.4 is also required.

* Added ignoreUnreadable flag to readOne and readComponents
* Tolerate date-time or date fields incorrectly failing to set VALUE=DATE
  for date values
* Cause unrecognized lines to default to use a text behavior, so commas,
  carriage returns, and semi-colons are escaped properly in unrecognized
  lines

vobject 0.4.4 released (SVN revision 159)
--
9 October 2006

To install, use _easy_install_, or download the archive and untar, run
`python setup.py install`.
_dateutil 1.1_ or later is required.
Python 2.4 is also required.

* Merged in Apple CalendarServer patches as of CalendarServer-r191
* Added copy and duplicate code to base module
* Improved recurring VTODO handling
* Save TZIDs when parsed and use them as back up TZIDs when serializing

vobject 0.4.3 released (SVN revision 157)
--
22 September 2006

To install, use _easy_install_, or download the archive and untar, run
`python setup.py install`.
_dateutil 0.9_ or later is required.
Python 2.4 is also required.

* Added support for PyTZ `tzinfo` classes.

vobject 0.4.2 released (SVN revision 153)
--
29 August 2006

To install, use _easy_install_, or download the archive and untar, run
`python setup.py install`.
_dateutil 0.9_ or later is required.
Python 2.4 is also required.

* Updated `ez_setup.py` to use the latest _setuptools_.

vobject 0.4.1 released (SVN revision 152)
--
4 August 2006

To install, use _easy_install_, or download the archive and untar, run
`python setup.py install`.
_dateutil 0.9_ or later is required.
Python 2.4 is also required.

* When vobject encounters ASCII, it now tries UTF-8, then UTF-16 with
  either LE or BE byte orders, searching for BEGIN in the decoded string
  to determine if it's found an encoding match. `readOne` and
  `readComponents` will no longer work on arbitrary Versit style ASCII
  streams unless the optional `findBegin` flag is set to `False`

vobject 0.4.0 released (SVN revision 151)
--
2 August 2006

To install, use _easy_install_, or download the archive and untar, run
`python setup.py install`.
_dateutil 0.9_ or later is required.
Python 2.4 is also required.

* Workarounds for common invalid files produced by Apple's iCal and AddressBook
* Added getChildValue convenience method
* Added experimental hCalendar serialization
* Handle DATE valued EXDATE and RRULEs better

vobject 0.3.0 released (SVN revision 129)
--
17 February 2006

To install, untar the archive, run `python setup.py install`.
_dateutil 0.9_ or later is required.
Python 2.4 is also required.

* Changed API for accessing children and parameters, attributes now
  return the first child or parameter, not a list. See usage for examples
* Added support for groups, a vcard feature
* Added behavior for FREEBUSY lines
* Worked around problem with dateutil's treatment of experimental
  properties (bug 4978)
* Fixed bug 4992, problem with rruleset when addRDate is set

vobject 0.2.3 released (SVN revision 104)
--
9 January 2006

To install, untar the archive, run `python setup.py install`.
_dateutil 0.9_ or later is required.
Python 2.4 is also required.

*
* Added VERSION line back into native iCalendar objects
* Added a first stab at a vcard module, parsing of vCard 3.0 files now
  gives structured values for N and ADR properties
* Fix bug in regular expression causing the '^' character to not parse

vobject 0.2.2 released (SVN revision 101)
--
4 November 2005

To install, untar the archive, run `python setup.py install`.
_dateutil 0.9_ or later is required.
Python 2.4 is also required.

* Fixed problem with add('duration')
* Fixed serialization of EXDATEs which are dates or have floating timezone
* Fixed problem serializing timezones with no daylight savings time

vobject 0.2.0 released (SVN revision 97)
--
10 October 2005

To install, untar the archive, run `python setup.py install`.
_dateutil 0.9_ or later is required.
Python 2.4 is also required.

* Added serialization of arbitrary tzinfo classes as VTIMEZONEs
* Removed unused methods
* Changed getLogicalLines to use regular expressions, dramatically
  speeding it up
* Changed rruleset behavior to use a property for rruleset

vobject 0.1.4 released (SVN revision 93)
--
30 September 2005

To install, untar the archive, run `python setup.py install`.
_dateutil 0.9_ or later is required.
Python 2.4 is also required.

* Changed parseLine to use regular expression instead of a state
  machine, reducing parse time dramatically

vobject 0.1.3 released (SVN revision 88)
--
1 July 2005

To install, untar the archive, run `python setup.py install`.
_dateutil 0.9_ or later is required.

* As of this release, Python 2.4 is required.
* Added license and acknowledgements.
* Fixed the fact that defaultSerialize wasn't escaping linefeeds
* Updated backslashEscape to encode CRLF's and bare CR's as linefeeds,
  which seems to be what RFC2445 requires

vobject 0.1.2 released (SVN revision 83)
--
24 March 2005

To install, untar the archive, run `python setup.py install`.
_dateutil_ is required.

* You'll need to apply this patch to be able to read certain VTIMEZONEs
  exported by Apple iCal, or if you happen to be in Europe!

  patch -R $PYTHONLIB/site-packages/dateutil/tz.py dateutil-0.5-tzoffset-bug.patch

* Fixed printing of non-ascii unicode.
* Fixed bug preventing content lines with empty contents from parsing.

vobject 0.1.1 released (SVN revision 82)
--
25 January 2005

To install, untar the archive, run `python setup.py install`.
`_dateutil_` is required.

* You'll need to apply this patch to be able to read certain VTIMEZONEs
  exported by Apple iCal, or if you happen to be in Europe!

  patch -R $PYTHONLIB/site-packages/dateutil/tz.py dateutil-0.5-tzoffset-bug.patch

* Various bug fixes involving recurrence.
* TRIGGER and VALARM behaviors set up.

vobject 0.1 released (SVN revision 70)
--
13 December 2004

* Parsing all iCalendar files should be working, please file a bug if
  you can't read one!
* Timezones can be set for datetimes, but currently they'll be converted
  to UTC for serializing, because VTIMEZONE serialization isn't yet
  working.
* RRULEs can be parsed, but when they're serialized, they'll be
  converted to a maximum of 500 RDATEs, because RRULE serialization
  isn't yet working.
* To parse unicode, see issue 4.
* Much more testing is needed, of course!
