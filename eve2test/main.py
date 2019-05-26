import os
import sys
import json

from collections import defaultdict, Mapping
import functools
import itertools

from eve2test import parser
from eve2test import context_managers as cxtm
from eve2test import valmap
from eve2test.exceptions import UnidentifiedValueError


skip_fields = ["timestamp"]


def perform_sanity_checks(eve_type):
    if eve_type not in valmap.event_types:
        raise UnidentifiedValueError(
                "Uh-oh! Unidentified type of event: {}".format(eve_type))


def filter_event_type_params(eve_rules, output_path):
    for _, category in itertools.groupby(
        eve_rules, key=lambda item:item['event_type']):
        for components in category:
            with cxtm.YamlIndenter() as yi:
                yi.write("- filter:", output_path)
                with yi:
                    with yi:
                        yi.write("count: 1", output_path)
                        yi.write("match:", output_path)
                        for component, val in components.items():
                            if component in skip_fields:
                                continue
                            if isinstance(val, Mapping):
                                yi.write("{}:".format(component), output_path)
                                for opt_k, opt_v in val.items():
                                    with yi:
                                        yi.write("{}: {}".format(opt_k, opt_v), output_path)
                            else:
                                yi.write("{}: {}".format(component, val), output_path)


def write_to_file(fpath, data):
    try:
        os.remove(fpath)
    except FileNotFoundError:
        print("{} not found. Creating...".format(fpath))
    with open(fpath, "a") as fp:
        fp.write(data)


def filter_event_type(event_types, output_path):
    """
    Filter based on the event types.
    """
    write_to_file(fpath=output_path, data="checks:\n")
    with cxtm.YamlIndenter() as yi:
        for event_t, event_c in event_types.items():
            yi.write("- filter:", output_path)
            with yi:
                with yi:
                    yi.write("count: {}".format(event_c), output_path)
                    yi.write("match:", output_path)
                    with yi:
                        yi.write("event_type: {}".format(event_t), output_path)


def process_eve(eve_path, output_path):
    """
    Process the provided eve.json file and return the desired results.
    """
    content = list()
    event_types = defaultdict(int)
    with open(eve_path, "r") as fp:
        for line in fp:
            eve_rule = json.loads(line)
            content.append(eve_rule)
            eve_type = eve_rule.get("event_type")
            perform_sanity_checks(eve_type=eve_type)
            event_types[eve_type] += 1

    filter_event_type(event_types=event_types, output_path=output_path)
    filter_event_type_params(eve_rules=content, output_path=output_path)


def main():
    eve_path, output_path = parser.parse_args()
    try:
        process_eve(eve_path=eve_path, output_path=output_path)
    except UnidentifiedValueError as uve:
        print(uve)
        sys.exit(1)
    print("Success")


if __name__ == "__main__":
    main()
