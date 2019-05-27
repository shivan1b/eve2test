import json
import logging
import os
import sys
from collections import Mapping, defaultdict

from eve2test import context_managers as cxtm
from eve2test import parser, valmap
from eve2test.exceptions import UnidentifiedValueError


# Get a logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Fields to exclude from the filter block
skip_fields = ["timestamp", "flow_id"]


def init_logger():
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def perform_sanity_checks(eve_type):
    """
    Check for valid event types.
    Raise an exception in case of unidentified event types.
    """
    if eve_type not in valmap.event_types:
        raise UnidentifiedValueError(
                "Uh-oh! Unidentified type of event: {}".format(eve_type))


def filter_event_type_params(eve_rules):
    """
    Create a filter block based on all the parameters of any event.

    This function uses YamlIndenter which kind of makes the code ugly
    but yaml.dump does not quite maintain the aesthetics of the dumped
    data. Developer OCD problems.
    """
    write_to_file(data="checks:\n")
    for components in eve_rules:
        with cxtm.YamlIndenter(fpath=output_path) as yi:
            yi.write("- filter:")
            with yi:
                with yi:
                    # Since the match is per component, the count shall
                    # always be 1.
                    yi.write("count: 1")
                    yi.write("match:")
                    with yi:
                        for component, val in components.items():
                            # Do not add fields defined by skip_fields variable
                            # to the filter block
                            if component in skip_fields:
                                continue
                            # If the val is a dict itself, write its components
                            # in the filter block too
                            if isinstance(val, Mapping):
                                yi.write("{}:".format(component))
                                for opt_k, opt_v in val.items():
                                    with yi:
                                        yi.write("{}: {}".format(opt_k, opt_v))
                            else:
                                yi.write("{}: {}".format(component, val))


def write_to_file(data):
    """
    Check for the output file if it exists, else create one and writw
    to it.
    """
    try:
        os.remove(output_path)
    except FileNotFoundError:
        logger.info("{} not found. Creating...".format(output_path))
    with open(output_path, "w+") as fp:
        fp.write("# *** Add configuration here ***\n\n")
        fp.write(data)


def filter_event_type(event_types):
    """
    Filter based only on the event types.

    This function uses YamlIndenter which kind of makes the code ugly
    but yaml.dump does not quite maintain the aesthetics of the dumped
    data. Developer OCD problems.
    """
    write_to_file(data="checks:\n")
    with cxtm.YamlIndenter(fpath=output_path) as yi:
        for event_t, event_c in event_types.items():
            yi.write("- filter:")
            with yi:
                with yi:
                    yi.write("count: {}".format(event_c))
                    yi.write("match:")
                    with yi:
                        yi.write("event_type: {}".format(event_t))


def process_eve(eve_path, alerttype_only):
    """
    Process the provided eve.json file and write the required checks in the
    provided output file.
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

    if alerttype_only:
        filter_event_type(event_types=event_types)
        return
    filter_event_type_params(eve_rules=content)


def main():
    global output_path
    args = vars(parser.parse_args())
    eve_path = args["path-to-eve"]
    output_path = args["output-path"]
    alerttype_only = args["alerttype_only"]
    init_logger()
    try:
        process_eve(eve_path=eve_path,
                alerttype_only=alerttype_only)
    except UnidentifiedValueError as uve:
        logger.error(uve)
        sys.exit(1)


if __name__ == "__main__":
    main()
