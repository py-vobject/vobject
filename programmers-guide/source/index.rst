.. vobject programmers guide
   Copyright (C) 2024, David Arnold

vObject
=======

.. toctree::
   :maxdepth: 3
   :caption: Contents:

Introduction
============
`vobject` is a pure-Python package for generating and parsing *vCard*
and *iCalendar* (aka *vCalendar*) objects, used for sharing and storage
of personal contacts and calendar events.

It supports Python 3.8 or later.  Releases in the 0.9.x series support
Python 2.7, and earlier releases of Python 3.

This document gives an overview of the *vCard* and *iCalendar* standards,
sufficient to begin using the package to generate or parse those that you
will likely encounter in general use.  And it explains the API, with
examples of common tasks.


.. #####################################################################

Quick Start
===========

Install ``vobject`` from PyPI using ``pip``, usually into a suitable
virtual environment:

.. code-block:: sh
    :linenos:

    pip install vobject

In all code examples in this chapter, we assume that the package has
been imported like this:

.. code-block:: python
    :linenos:

    import vobject

You can parse an existing contact (typically ``.vcf``) or calendar
(typically ``.ics``) file, and get an iterator to the contained
objects:

.. code-block:: python
    :linenos:

    with open("my-cards-file.vcf") as vo_stream:
        for vo in vobject.readComponents(vo_stream):
            vo.prettyPrint()

If you only want to read a single object, you can use ``readOne()``
rather than ``readComponents()``.

Given a Python instance of a vObject, you can then perform many
operations on it.

You can get its name:

.. code-block:: python
    :linenos:

    >>> print(item.name)
    VCARD
    >>>

Get its children (if any):

.. code-block:: python
    :linenos:

    >>> list(item.getChildren())

or get its children in sorted order (alphabetic, except for the required
children in the standard-specified order):

.. code-block:: python
    :linenos:

    >>> list(item.getSortedChildren())

When there are no children, an empty list is returned.

A component's children can be accessed through these generators (as
above), or using a function:

.. code-block:: python
    :linenos:

    >>> print(item.getChildValue("version")
    3.0
    >>>

Or using the ``contents`` dictionary:

.. code-block:: python
    :linenos:

    >>> print(item.contents["version"][0].value)
    3.0
    >>>

Note two things when accessing the item's properties via the ``contents``
dictionary: first, the dictionary is a collection is *lists*, so even
singleton property values need to access the first list element, and
second, the object in the list is a class that holds the actual value,
accessed using the ``value`` attribute (there are other attributes of
the value available from that class instance as well).

Or using their names to access them directly as attributes:

.. code-block:: python
    :linenos:

    >>> print(item.version.value)
    3.0
    >>>

When accessed as named attributes of the parsed item, singleton
properties *aren't* a list: you can access their value directly.  If
the child has parameters, in addition to its value, they are available
as a dictionary:

.. code-block:: python
    :linenos:

    >>> print(item.contents["adr"][0].params)
    {'TYPE': ['WORK', 'pref']}
    >>>

Some values are structured types: names (NAME) and addresses (ADR) in
vCards, for example:

.. code-block:: python
    :linenos:

    >>> address = item.contents["adr"][0].value
    >>> print(address.street)
    42 Main Street
    >>> print(address.country)
    USA
    >>>

vObjects can be created by parsing (as above), or by using a helper
function:

.. code-block:: python
    :linenos:

    >>> my_card = vobject.vCard()

or using the registry of known component types:

.. code-block:: python
    :linenos:

    >>> my_todo = vobject.newFromBehavior("vtodo")

Having created, and then populated a vobject as required, you can
generate its serialized string format:

.. code-block:: python
    :linenos:

    >>> entry = vobject.newFromBehavior("vjournal")
    >>> entry.add("summary").value = "Summary"
    >>> entry.add("description").value = "The whole description"
    >>>
    >>> entry.serialize()
    'BEGIN:VJOURNAL\r\nDESCRIPTION:The whole description\r\n'
    'DTSTAMP:20240331T013220Z\r\nSUMMARY:Summary\r\n'
    'UID:20240331T015748Z - 66283@laptop.local\r\nEND:VJOURNAL\r\n'
    >>>

(the serialized value has been split over several lines for clarity: it
is a single string, shown on a single line, in the original interpreter
output).

Note that ``vobject`` has added the mandatory ``UID`` and ``DTSTAMP``
components during serialization.


.. #####################################################################

Installing
==========

``vobject`` is distributed via PyPI_ or from GitHub_.  For most people,
using ``pip`` and PyPI is easiest and best way to install, but other
options and reasons to use them are discussed in this chapter.

PyPI
----
You can install ``vobject`` using ``pip``:

.. code-block:: shell

    $ pip install vobject

It's usually a good idea to install ``vobject`` into a virtual
environment, to avoid issues with incompatible versions and system-wide
packaging schemes.

Installing using ``pip`` this way will also install ``vobject``'s
runtime dependencies, so it should be immediately ready for use.

Other Options
-------------
``vobject`` is distributed as a universal *wheel*, and should install
from PyPI using ``pip`` without difficulty in most cases.  There is
also an *sdist* available from PyPI and GitHub which can be used as a
fallback.

If your development environment cannot access PyPI for some reason,
then downloading the *wheel* (or *sdist*) from a machine with Internet
access, and transferring to your development environment would make
sense.

Alternatively, you can clone the source repository from GitHub using
git_.  If you're intending to modify ``vobject`` and potentially
contribute those changes back to the project, you should use the
``git clone`` method.

Finally, the latest package source code for any release can be
downloaded from GitHub as either a ``tar`` or ``zip`` file.  This
is probably not useful in the majority of cases, but it might be
useful to archive the source code for auditing or similar purposes.

Installing a wheel
~~~~~~~~~~~~~~~~~~
If you've downloaded a *wheel* file (it should have a ``.whl`` suffix),
you can install it using ``pip`` as well:

.. code-block:: shell

    $ pip install <wheel-file-name>.whl

Using this method, ``pip`` will automatically try to satisfy the runtime
dependencies by downloading their wheels in turn, unless they're already
available in the target (virtual) environment.  But it will work fine
without access to PyPI if the required dependencies are already
installed.

Installing an sdist (source distribution)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A Python *sdist* (source distribution) is a tar file (with extension
``.tar.gz``) produced as part of making a Python package.  It is very
easily confused with the source *code* distribution, because the names
are basically identical, and both can have the same file extension.

*sdist* files can be downloaded from PyPI or from GitHub, and
will have a name like ``vobject-0.9.7.tar.gz``.  At GitHub, this file
is listed with that filename under the release assets and **NOT** as
the link called *"Source code (tar.gz)"*.

You can download the *sdist* manually, and then install it with ``pip``:

.. code-block:: shell

    $ pip install <sdist-file-name>.tar.gz

Installing from cloned source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you want to use a cloned source repository, likely the best way to
install ``vobject`` is to use ``pip``'s editable install mechanism.

First, activate the virtual environment to be used for development,
and install using ``pip`` like:

.. code-block::

    $ git clone git://github.com/py-vobject/vobject.git
    $ cd vobject
    $ pip install -e .

This will collect, build, and install the dependencies (from PyPI) and
then install an *editable* version of the ``vobject`` package (that's
the ``-e`` parameter).  An editable install directly uses the files in
your checkout area, including any local modifications you've made at
the time you imported the package.


.. #####################################################################

Importing
=========

You can import the ``vobject`` module maintaining its internal structure,
or you can import some or all bindings directly.

.. index:: vobject, vCard
.. code-block:: python
    :linenos:

    import vobject

    card = vobject.vCard()


Or

.. code-block:: python
    :linenos:

    from vobject import *

    card = vCard()


All the example code in this document will use the first form, which is
strongly recommended.

.. index:: import, namespace

Note that the ``import *`` form is explicitly supported, with the
exposed namespace controlled to contain only the public features
of the package.


.. #####################################################################

Calendars and Cards
===================

.. index:: Apple, AT&T, IBM, IETF, Internet Mail Consortium, Lucent, Siemens, Versit Consortium
.. index:: vCard, vCalendar, iCalendar

The *vCard* and *vCalendar* specifications were originally developed
by the Versit Consortium (and that's why they're named with a leading
"v"), with contributions from Apple, IBM, AT&T/Lucent, and Siemens.
Their stewardship subsequently passed to the Internet Mail Consortium,
before the standards were later adopted by the IETF.

Within the IETF, vCard versions 3.0 and 4.0, and a revised and expanded
calendar specification renamed to *iCalendar* 2.0 have been published,
together with numerous extensions, clarifications, and related standards.

The two main standards (vCard and iCalendar) form a way to store and
communicate information about contacts (names, addresses, phone numbers,
etc), and scheduling (events, todos, etc).  They have been widely
adopted for both storage and sharing of contact and calendar data.

vCard
-----

.. index:: RFC-2426, RFC-6350

vCard 2.1 was the final version published by Versit, and is still widely
used.  vCard 3.0, published as IETF RFC-2426, is also widely used, however
both versions are frequently extended by vendors or have implementation
quirks in part due to unclear specification.  vCard 4.0 (IETF RFC-6350)
attempted to resolve the issues of earlier versions, but in doing so
necessarily broke some backward compatibility, and as a result, it has
not been universally adopted.

iCalendar
---------

.. index:: CalDAV, RFC-2445

vCalendar 1.0 was published by Versit, however it was not until the
renamed iCalendar 2.0 (IETF RFC-2445) was published that wide-spread
interoperability was possible.  Together with various extensions, and in
particular the CalDAV specification for sharing calendars, iCalendar is
now almost universally used for communication of calendaring data.

Related Standards
-----------------

.. index:: JSON, microformat, XML

Alongside vCard and iCalendar several different formats have been
developed that reuse most (or all) of their semantic model, while
adopting a different syntax.  XML and JSON variants of both standards
exist, as well as HTML microformats.

More recent work in the IETF is looking to revise the semantic models
of vCard and iCalendar, proposing new standards that can be translated
to and from vCard and iCalendar, but add extra functionality.

vObject
-------

The Python ``vobject`` module supports parsing vCard and iCalendar objects
from strings (email attachments, files, etc) and generating those
formatted strings from Python card and calendar objects.  It maintains
compatibility with older versions of the specifications, and supports
various quirks of widely-used implementations, simplifying real-life
usage.

.. index:: Open Source Applications Foundation, OSAF, Chandler, Eventable, GitHub, Apache
.. index:: single: Harris, Jeffrey
.. index:: single: Karim, Sameen

``vobject`` was originally developed by Jeffrey Harris, working at the Open
Source Applications Foundation (OSAF) on their Chandler project.  It was
subsequently adopted by Sameen Karim at Eventable, before passing to
community maintenance.  The source code is freely available under the
Apache 2.0 license, and developed in a public repository at GitHub.

Model
-----

.. index:: MIME, email

*iCalendar* and *vCard* are both Multipurpose Internet Mail Extension
(MIME) *profiles*.  Originally designed as a way to attach files to
emails, the MIME standards include profiles for various types of
things that are attached to emails from files, including calendar
events and contacts, allowing email clients to understand what they
are, and how to decode them.

Over time, the use of MIME types and their encoding/decoding standards
has extended beyond email, particularly to web browsers, and to
operating systems in general, where the concept of a "default
application" for a MIME type is used to open downloaded files.

.. index:: JSON, XML

*iCalendar* and *vCard* share a MIME syntax and basic encoding
mechanism that is worth explaining up front because it's a little
different to more recent alternatives such as JSON or XML.

.. index:: enclosure, component, content line, parameter, value

The major elements of the model are:

* Enclosure
* Components
* Content Lines
* Parameters
* Values

Each of these is discussed in detail below.  It's not *necessary* to
understand the full detail of these elements, but you will need at
least an overview to work with the ``vobject`` API.

Enclosure
~~~~~~~~~

A MIME *enclosure* (for example, an ``.ics`` file) is an ordered
sequence of octets, formatted in accordance with a standard MIME
profile.  For the *iCalendar* and *vCard* profiles, the MIME
enclosure's contents can be identified in one of two ways: using
``PROFILE`` or using ``BEGIN`` and ``END``.

When using ``PROFILE``, only one object can be encoded within the MIME
enclosure.  The octet stream contains an initial text line beginning
with "``PROFILE``" that defines the type of the object described by
the following lines.  All lines in the MIME enclosure refer to a single
object of the profile type.

More commonly, using ``BEGIN`` and ``END`` allows multiple objects to
be encoded into a single MIME enclosure.  This is usually used for
both *iCalendar* and *vCard*, but the ``PROFILE`` format is also
supported by ``vobject``.

Component
~~~~~~~~~

Within the enclosure then, one or more objects are encoded.  Each
object is called a *component* which represents a complete entity: a
person, an event, a journal entry, a timezone, etc.  Components are
described by a set of properties possibly including other nested
components.

The type of the component is identified by either the ``PROFILE`` or
the ``BEGIN`` / ``END`` lines, for example like:

.. code-block::

   BEGIN:VCARD
   ...
   END:VCARD

The component types used by the *iCalendar* and *vCard* standards
include:

* ``VCALENDAR``
* ``VEVENT``
* ``VTODO``
* ``VJOURNAL``
* ``VTIMEZONE``
* ``VFREEBUSY``
* ``VALARM``
* ``VCARD``

Content Line
~~~~~~~~~~~~

A MIME enclosure exists as a sequence of octets (bytes).  These octets
represent characters, using a specified *character encoding* --
typically UTF-8 in modern usage, but possibly ASCII, or other
language-specific encodings, depending on the source application.

That sequence of characters is broken into *physical lines* by the
character pair ``CRLF``: a *Carriage Return*, followed by a *Line
Feed*.  The strings of characters separated by ``CRLF`` pairs are the
physical lines.

According to the specification, physical lines should not exceed 80
octets, including the ``CRLF``.  Because the content itself might
exceed that length, encoding first breaks the content into shorter
lines (called *folding*), and decoding must reassemble the content
from those broken up physical lines (called *unfolding*).

The unfolded content, possibly longer than 80 octets, is called a
*content line*.  Each content line within a component describes a
property of that component.

A content line has a name, usually written in ALL CAPS style.  It may
also have zero or more *parameters*, and finally a *value*.

Parameters
~~~~~~~~~~

The optional parameters of a content line either describe its encoding,
or clarify its meaning within the component.  Parameters have a name,
and optional set of parameter values.

Example parameters include things like the BASE64 encoding of a
contact's photgraph, or the type of a phone number: voice, fax, work,
home, etc.

Some properties are represented just by their name, like ``JPEG``,
while others have one or more parameter values, like ``TZID=EST``.

Value
~~~~~

Finally, the content line will have a value.  The formatting of the
value depends upon what property type is represents, and it might be
either a single simple type, a sequence, or a complex multi-part
object.

For exmaple, the ``VERSION`` property has a single, string-type value.

.. code-block::

   VERSION:3.0

But a *vCard* name property has a complex type value, with five
different attributes, separated by semi-colons:

.. code-block::

   N:Public;John;Quinlan;Mr;Esq

The types of values for each standard property are defined by the
standard documents, and implemented by ``vobject``.


.. #####################################################################

Parsing
=======

To parse one top level component from an existing *iCalendar* or
*vCard* stream or string, use the ``readOne()`` function:

.. code-block:: python
    :linenos:

    >>> parsedCal = vobject.readOne(icalstream)
    >>> parsedCal.vevent.dtstart.value
    datetime.datetime(2006, 2, 16, 0, 0, tzinfo=tzutc())

Similarly, ``readComponents()`` is a generator yielding one top level
component at a time from a stream or string.

.. code-block:: python
    :linenos:

    >>> vobject.readComponents(icalstream).next().vevent.dtstart.value
    datetime.datetime(2006, 2, 16, 0, 0, tzinfo=tzutc())

Parsing vCards is very similar.

.. code-block:: python
    :linenos:

    >>> s = """
    ... BEGIN:VCARD
    ... VERSION:3.0
    ... EMAIL;TYPE=INTERNET:jeffrey@osafoundation.org
    ... EMAIL;TYPE=INTERNET:jeffery@example.org
    ... ORG:Open Source Applications Foundation
    ... FN:Jeffrey Harris
    ... N:Harris;Jeffrey;;;
    ... END:VCARD
    ... """
    >>> v = vobject.readOne( s )
    >>> v.prettyPrint()
     VCARD
        ORG: Open Source Applications Foundation
        VERSION: 3.0
        EMAIL: jeffrey@osafoundation.org
        params for  EMAIL:
           TYPE [u'INTERNET']
        FN: Jeffrey Harris
        N:  Jeffrey  Harris
    >>> v.n.value.family
    u'Harris'
    >>> v.email_list
    [<EMAIL{'TYPE': ['INTERNET']}jeffrey@osafoundation.org>,
     <EMAIL{'TYPE': ['INTERNET']}jeffery@example.org>]

Just like with the *iCalendar* example above, ``readComponents()`` will
yield a generator from a stream or string containing multiple *vCard*
objects.

.. code-block:: python
    :linenos:

    >>> vobject.readComponents(vCardStream).next().email.value
    'jeffrey@osafoundation.org'


.. #####################################################################

Creating Objects
================

iCalendar
---------

vObject has a basic datastructure for working with iCalendar-like
syntax.  Additionally, it defines specialized behaviors for many of
the standard iCalendar components.

The iCalendar standard defines six object types:

* VEVENT
* VTODO
* VJOURNAL
* VTIMEZONE
* VFREEBUSY
* VALARM

plus the containing VCALENDAR object (note the name, a hold-over from
the v1.0 Versit standard).

An iCalendar stream (eg. an .ics file) is comprised of a sequence of
these objects.

Within vobject, each standard object has a defined *behavior* class,
that specifies its allowed cardinality, base data type, ability to
convert to/from native Python data types, etc.  These behaviors are
maintained in a registry within the vobject module, and identified by
name.

To create an object that already has a behavior defined, run:

.. index:: newFromBehavior
.. code-block:: python
    :linenos:

    >>> import vobject
    >>> cal = vobject.newFromBehavior('vcalendar')
    >>> cal.behavior
    <class 'vobject.icalendar.VCalendar2_0'>

Convenience functions exist to create iCalendar and vCard objects:

.. code-block:: python
    :linenos:

    >>> cal = vobject.iCalendar()
    >>> cal.behavior
    <class 'vobject.icalendar.VCalendar2_0'>
    >>> card = vobject.vCard()
    >>> card.behavior
    <class 'vobject.vcard.VCard3_0'>

Once you have an object, you can use the add method to create
children:

.. index:: add, prettyPrint
.. code-block:: python
    :linenos:

    >>> cal.add('vevent')
    <VEVENT| []>
    >>> cal.vevent.add('summary').value = "This is a note"
    >>> cal.prettyPrint()
     VCALENDAR
        VEVENT
           SUMMARY: This is a note

Note that summary is a little different from vevent, it's a
ContentLine, not a Component.  It can't have children, and it has a
special value attribute.

ContentLines can also have parameters.  They can be accessed with
regular attribute names with _param appended:

.. code-block:: python
    :linenos:

    >>> cal.vevent.summary.x_random_param = 'Random parameter'
    >>> cal.prettyPrint()
     VCALENDAR
        VEVENT
           SUMMARY: This is a note
           params for  SUMMARY:
              X-RANDOM ['Random parameter']

There are a few things to note about this example

  * The underscore in x_random is converted to a dash (dashes are
    legal in iCalendar, underscores legal in Python)
  * X-RANDOM's value is a list.

If you want to access the full list of parameters, not just the first,
use &lt;paramname&gt;_paramlist:

.. code-block:: python
    :linenos:

    >>> cal.vevent.summary.x_random_paramlist
    ['Random parameter']
    >>> cal.vevent.summary.x_random_paramlist.append('Other param')
    >>> cal.vevent.summary
    <SUMMARY{'X-RANDOM': ['Random parameter', 'Other param']}This is a note>

Similar to parameters, If you want to access more than just the first
child of a Component, you can access the full list of children of a
given name by appending `_list` to the attribute name:

.. code-block:: python
    :linenos:

    >>> cal.add('vevent').add('summary').value = "Second VEVENT"
    >>> for ev in cal.vevent_list:
    ...     print ev.summary.value
    This is a note
    Second VEVENT

The interaction between the del operator and the hiding of the
underlying list is a little tricky, del cal.vevent and del
cal.vevent_list both delete all vevent children:

.. code-block:: python
    :linenos:

    >>> first_ev = cal.vevent
    >>> del cal.vevent
    >>> cal
    <VCALENDAR| []>
    >>> cal.vevent = first_ev

VObject understands Python's datetime module and tzinfo classes.

.. code-block:: python
    :linenos:

    >>> import datetime
    >>> utc = vobject.icalendar.utc
    >>> start = cal.vevent.add('dtstart')
    >>> start.value = datetime.datetime(2006, 2, 16, tzinfo = utc)
    >>> first_ev.prettyPrint()
         VEVENT
            DTSTART: 2006-02-16 00:00:00+00:00
            SUMMARY: This is a note
            params for  SUMMARY:
               X-RANDOM ['Random parameter', 'Other param']

Components and ContentLines have serialize methods:

.. code-block:: python
    :linenos:

    >>> cal.vevent.add('uid').value = 'Sample UID'
    >>> icalstream = cal.serialize()
    >>> print icalstream
    BEGIN:VCALENDAR
    VERSION:2.0
    PRODID:-//PYVOBJECT//NONSGML Version 1//EN
    BEGIN:VEVENT
    UID:Sample UID
    DTSTART:20060216T000000Z
    SUMMARY;X-RANDOM=Random parameter,Other param:This is a note
    END:VEVENT
    END:VCALENDAR

Observe that serializing adds missing required lines like version and
prodid.  A random UID would be generated, too, if one didn't exist.

If dtstart's tzinfo had been something other than UTC, an appropriate
vtimezone would be created for it.

vCard
-----

Making vCards proceeds in much the same way. Note that the 'N' and 'FN'
attributes are required.

.. code-block:: python
    :linenos:

    >>> j = vobject.vCard()
    >>> j.add('n')
     <N{}    >
    >>> j.n.value = vobject.vcard.Name( family='Harris', given='Jeffrey' )
    >>> j.add('fn')
     <FN{}>
    >>> j.fn.value ='Jeffrey Harris'
    >>> j.add('email')
     <EMAIL{}>
    >>> j.email.value = 'jeffrey@osafoundation.org'
    >>> j.email.type_param = 'INTERNET'
    >>> j.add('org')
     <ORG{}>
    >>> j.org.value = ['Open Source Applications Foundation']
    >>> j.prettyPrint()
     VCARD
        ORG: ['Open Source Applications Foundation']
        EMAIL: jeffrey@osafoundation.org
        params for  EMAIL:
           TYPE ['INTERNET']
        FN: Jeffrey Harris
        N:  Jeffrey  Harris

serializing will add any required computable attributes (like 'VERSION')

.. code-block:: python
    :linenos:

    >>> j.serialize()
    'BEGIN:VCARD\r\nVERSION:3.0\r\nEMAIL;TYPE=INTERNET:jeffrey@osafoundation.org\r\nFN:Jeffrey Harris\r\nN:Harris;Jeffrey;;;\r\nORG:Open Source Applications Foundation\r\nEND:VCARD\r\n'
    >>> j.prettyPrint()
     VCARD
        ORG: Open Source Applications Foundation
        VERSION: 3.0
        EMAIL: jeffrey@osafoundation.org
        params for  EMAIL:
           TYPE ['INTERNET']
        FN: Jeffrey Harris
        N:  Jeffrey  Harris



.. #####################################################################

Common Problems
===============

- Non-ASCII characters
- Selecting a serialization format version
- Validation
- Flags controlling compatibility with popular application's bugs



.. #####################################################################

Getting Help
============

TBD

.. _GitHub: https://github.com/py-vobject/vobject
.. _Python: http://www.python.org/
.. _PyPI: https://pypi.org/project/vobject/
.. _pip: http://www.pip-installer.org/
.. _git: https://git-scm.com/
