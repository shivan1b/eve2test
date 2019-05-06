import sys
import json

from eve2test import parser
from eve2test import context_managers as cxtm
from eve2test import valmap
from eve2test.exceptions import UnidentifiedValueError


class Event(dict):
    """
    Define class for overridden behavior of the usual Python dict.
    """
    def __missing__(self, key):
        """
        In case a key is missing, its count is set to 0 instead of the usual
        KeyError.
        """
        return 0


def perform_sanity_checks(eve_type):
    if eve_type not in valmap.event_types:
        raise UnidentifiedValueError(
                "Uh-oh! Unidentified type of event: {}".format(eve_type))


def filter_event_type(event_types):
    """
    Filter based on the event types.
    """
    print("checks:")
    with cxtm.YamlIndenter() as yi:
        for event_t, event_c in event_types.items():
            yi.print("- filter:")
            with yi:
                with yi:
                    yi.print("count: {}".format(event_c))
                    yi.print("match:")
                    with yi:
                        yi.print("event_type: {}".format(event_t))


def process_eve(path):
    """
    Process the provided eve.json file and return the desired results.
    """
    content = list()
    event_types = Event()
    with open(path, "r") as fp:
        for line in fp:
            eve_rule = json.loads(line)
            content.append(eve_rule)
            eve_type = eve_rule.get("event_type")
            perform_sanity_checks(eve_type=eve_type)
            event_types[eve_type] += 1

    filter_event_type(event_types=event_types)


def main():
    eve_path, output_path = parser.parse_args()
    try:
        process_eve(path=eve_path)
    except UnidentifiedValueError as uve:
        print(uve)
        sys.exit(1)
    print("Success")


if __name__ == "__main__":
    main()
