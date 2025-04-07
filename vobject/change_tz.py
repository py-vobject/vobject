"""Translate an ics file's events to a different timezone."""

from argparse import ArgumentParser
from datetime import datetime

import pytz
from dateutil import tz

import vobject

version = vobject.VERSION


def change_tz(cal, new_timezone, default, utc_only=False, utc_tz=vobject.icalendar.utc):
    """
    Change the timezone of the specified component.

    Args:
        cal (Component): the component to change
        new_timezone (tzinfo): the timezone to change to
        default (tzinfo): a timezone to assume if the dtstart or dtend in cal doesn't have an existing timezone
        utc_only (bool): only convert dates that are in utc
        utc_tz (tzinfo): the tzinfo to compare to for UTC when processing utc_only=True
    """

    for vevent in getattr(cal, "vevent_list", []):
        start = getattr(vevent, "dtstart", None)
        end = getattr(vevent, "dtend", None)
        for node in (start, end):
            if node:
                dt = node.value
                if isinstance(dt, datetime) and (not utc_only or dt.tzinfo == utc_tz):
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=default)
                    node.value = dt.astimezone(new_timezone)


def show_timezones():
    for tz_string in pytz.all_timezones:
        print(tz_string)


def convert_events(utc_only, ics_file, timezone_="UTC"):
    print(f'Converting {"only UTC" if utc_only else "all"} events')

    print(f"... Reading {ics_file}")
    with open(ics_file, "r") as f:
        cal = vobject.readOne(f)
    change_tz(cal, new_timezone=tz.gettz(timezone_), default=tz.gettz("UTC"), utc_only=utc_only)

    out_name = f"{ics_file}.converted"
    print(f"... Writing {out_name}")
    with open(out_name, "wb") as out:
        cal.serialize(out)

    print("Done")


def main():
    args = get_arguments()
    if args.list:
        show_timezones()
    elif args.ics_file:
        convert_events(utc_only=args.utc, ics_file=args.ics_file, timezone_=args.timezone)


def get_arguments():
    # Configuration options
    parser = ArgumentParser(description="change_tz will convert the timezones in an ics file.")
    parser.add_argument("-V", "--version", action="version", version=vobject.VERSION)

    parser.add_argument(
        "-u", "--only-utc", dest="utc", action="store_true", default=False, help="Only change UTC events."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-l", "--list", dest="list", action="store_true", default=False, help="List available timezones")
    group.add_argument("ics_file", nargs="?", help="The ics file to process")
    parser.add_argument("timezone", nargs="?", default="UTC", help="The timezone to convert to")

    return parser.parse_args()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Aborted")
