"""
Compare VTODOs and VEVENTs in two iCalendar sources.
"""

from argparse import ArgumentParser

import vobject


def getSortKey(component):
    def getUID(component):
        return component.getChildValue("uid", "")

    # it's not quite as simple as getUID, need to account for recurrenceID and sequence

    def getSequence(component) -> str:
        sequence = component.getChildValue("sequence", 0)
        return f"{int(sequence):05d}"

    def getRecurrenceID(component):
        recurrence_id = component.getChildValue("recurrence_id", None)
        if recurrence_id is None:
            return "0000-00-00"
        else:
            return recurrence_id.isoformat()

    return getUID(component) + getSequence(component) + getRecurrenceID(component)


def sortByUID(components):
    return sorted(components, key=getSortKey)


def deleteExtraneous(component, ignore_dtstamp=False):
    """
    Recursively walk the component's children, deleting extraneous details like
    X-VOBJ-ORIGINAL-TZID.
    """
    for comp in component.components():
        deleteExtraneous(comp, ignore_dtstamp)
    for line in component.lines():
        if "X-VOBJ-ORIGINAL-TZID" in line.params:
            del line.params["X-VOBJ-ORIGINAL-TZID"]
    if ignore_dtstamp and hasattr(component, "dtstamp_list"):
        del component.dtstamp_list


def diff(left, right):
    """
    Take two VCALENDAR components, compare VEVENTs and VTODOs in them,
    return a list of object pairs containing just UID and the bits
    that didn't match, using None for objects that weren't present in one
    version or the other.

    When there are multiple ContentLines in one VEVENT, for instance many
    DESCRIPTION lines, such lines original order is assumed to be
    meaningful.  Order is also preserved when comparing (the unlikely case
    of) multiple parameters of the same type in a ContentLine

    """

    def processComponentLists(leftList, rightList):
        output = []
        rightIndex = 0
        rightListSize = len(rightList)

        for comp in leftList:
            if rightIndex >= rightListSize:
                output.append((comp, None))
            else:
                leftKey = getSortKey(comp)
                rightComp = rightList[rightIndex]
                rightKey = getSortKey(rightComp)
                while leftKey > rightKey:
                    output.append((None, rightComp))
                    rightIndex += 1
                    if rightIndex >= rightListSize:
                        output.append((comp, None))
                        break
                    rightComp = rightList[rightIndex]
                    rightKey = getSortKey(rightComp)

                if leftKey < rightKey:
                    output.append((comp, None))
                elif leftKey == rightKey:
                    rightIndex += 1
                    matchResult = processComponentPair(comp, rightComp)
                    if matchResult is not None:
                        output.append(matchResult)
                        
        while rightIndex < rightListSize:
            output.append((None, rightList[rightIndex]))
            rightIndex += 1
            
        return output

    def newComponent(name, body):  # pylint:disable=unused-variable
        if body is None:
            return None
        c = vobject.base.Component(name)
        c.behavior = vobject.base.getBehavior(name)
        c.isNative = True
        return c

    def processComponentPair(leftComp, rightComp):
        """
        Return None if a match, or a pair of components including UIDs and
        any differing children.

        """
        leftChildKeys = leftComp.contents.keys()
        rightChildKeys = rightComp.contents.keys()

        differentContentLines = []
        differentComponents = {}

        for key in leftChildKeys:
            rightList = rightComp.contents.get(key, [])
            if isinstance(leftComp.contents[key][0], vobject.base.Component):
                compDifference = processComponentLists(leftComp.contents[key], rightList)
                if len(compDifference) > 0:
                    differentComponents[key] = compDifference

            elif leftComp.contents[key] != rightList:
                differentContentLines.append((leftComp.contents[key], rightList))

        for key in rightChildKeys:
            if key not in leftChildKeys:
                if isinstance(rightComp.contents[key][0], vobject.base.Component):
                    differentComponents[key] = ([], rightComp.contents[key])
                else:
                    differentContentLines.append(([], rightComp.contents[key]))

        if not differentContentLines and not differentComponents:
            return None

        left = vobject.newFromBehavior(leftComp.name)
        right = vobject.newFromBehavior(leftComp.name)
        # add a UID, if one existed, despite the fact that they'll always be
        # the same
        uid = leftComp.getChildValue("uid")
        if uid is not None:
            left.add("uid").value = uid
            right.add("uid").value = uid

        for name, childPairList in differentComponents.items():
            leftComponents, rightComponents = zip(*childPairList)
            if len(leftComponents) > 0:
                # filter out None
                left.contents[name] = filter(None, leftComponents)
            if len(rightComponents) > 0:
                # filter out None
                right.contents[name] = filter(None, rightComponents)

        for leftChildLine, rightChildLine in differentContentLines:
            nonEmpty = leftChildLine or rightChildLine
            name = nonEmpty[0].name
            if leftChildLine is not None:
                left.contents[name] = leftChildLine
            if rightChildLine is not None:
                right.contents[name] = rightChildLine

        return left, right

    vevents = processComponentLists(
        sortByUID(getattr(left, "vevent_list", [])), sortByUID(getattr(right, "vevent_list", []))
    )

    vtodos = processComponentLists(
        sortByUID(getattr(left, "vtodo_list", [])), sortByUID(getattr(right, "vtodo_list", []))
    )

    return vevents + vtodos


def prettyDiff(leftObj, rightObj):
    for left, right in diff(leftObj, rightObj):
        print("<<<<<<<<<<<<<<<")
        if left is not None:
            left.prettyPrint()
        print("===============")
        if right is not None:
            right.prettyPrint()
        print(">>>>>>>>>>>>>>>")


def main():
    args = get_arguments()
    with open(args.ics_file1) as f, open(args.ics_file2) as g:
        cal1 = vobject.readOne(f)
        cal2 = vobject.readOne(g)
    deleteExtraneous(cal1, ignore_dtstamp=args.ignore)
    deleteExtraneous(cal2, ignore_dtstamp=args.ignore)
    prettyDiff(cal1, cal2)


def get_arguments():
    # Configuration options #
    parser = ArgumentParser(description="ics_diff will print a comparison of two iCalendar files")
    parser.add_argument("-V", "--version", action="version", version=vobject.VERSION)
    parser.add_argument(
        "-i",
        "--ignore-dtstamp",
        dest="ignore",
        action="store_true",
        default=False,
        help="ignore DTSTAMP lines [default: False]",
    )
    parser.add_argument("ics_file1", help="The first ics file to compare")
    parser.add_argument("ics_file2", help="The second ics file to compare")

    return parser.parse_args()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Aborted")
