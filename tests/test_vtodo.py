import datetime
import io

import vobject

text = (
    "BEGIN:VCALENDAR\r\n"
    "VERSION:2.0\r\n"
    "PRODID:-//Example Corp.//CalDAV Client//EN\r\n"
    "BEGIN:VTODO\r\n"
    "UID:20070313T123432Z-456553@example.com\r\n"
    "DTSTAMP:20070313T123432Z\r\n"
    "DUE;VALUE=DATE:20070501\r\n"
    "SUMMARY:Submit Quebec Income Tax Return for 2006\r\n"
    "CLASS:CONFIDENTIAL\r\n"
    "CATEGORIES:FAMILY,FINANCE\r\n"
    "STATUS:NEEDS-ACTION\r\n"
    "END:VTODO\r\n"
    "END:VCALENDAR\r\n"
)


def test_vtodo():
    """
    Test VTodo
    """
    obj = vobject.readOne(io.StringIO(text))
    obj.vtodo.add("completed")
    obj.vtodo.completed.value = datetime.datetime(2015, 5, 5, 13, 30)
    assert obj.vtodo.completed.serialize()[0:23] == "COMPLETED:20150505T1330"

    obj = vobject.readOne(obj.serialize())
    assert obj.vtodo.completed.value == datetime.datetime(2015, 5, 5, 13, 30)
