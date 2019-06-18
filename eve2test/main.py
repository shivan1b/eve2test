import json
import yaml
import logging
import os
import sys
from collections import defaultdict
from yaml.representer import Representer

from eve2test import parser


# Get a logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Fields to exclude from the filter block
skip_fields = ["timestamp", "flow_id", "last_reload"]

yaml.add_representer(defaultdict, Representer.represent_dict)


def init_logger():
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def get_manipulated_list(event_type_only=False):
    with open(eve_path, "r") as fp:
        content = fp.read()
    content_list = content.strip().split("\n")
    manip_list1 = [json.loads(e) for e in content_list]
    manip_list2 = []
    for e in manip_list1:
        md = {k: v for k, v in e.items() if k not in skip_fields}
        manip_list2.append(md)

    final_list = []
    for item in manip_list2:
        mdict = {
            "filter": {
                "count": 1,
                "match": item,
                },
                }
        final_list.append(mdict)
    mydict = {"checks": final_list}
    return mydict


def filter_event_type_params(eve_rules):
    """
    Create a filter block based on all the parameters of any event.
    """
    mlist = get_manipulated_list()
    ydump = yaml.dump(mlist, default_flow_style=False)
    write_to_file(data=ydump)


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
    """
    final_list = []
    for k, v in event_types.items():
        mdict = {
            "filter": {
                "count": v,
                "match": {
                    "event_type": k,
                    },
                },
                }
        final_list.append(mdict)
    mydict = {"checks": final_list}
    ydump = yaml.dump(mydict, default_flow_style=False)
    write_to_file(data=ydump)


def process_eve(eve_path, eventtype_only):
    """
    Process the provided eve.json file and write the required checks in the
    provided output file.
    """
    content = list()
    allowed_event_types = eventtype_only.split(",")
    event_types = defaultdict(int)
    with open(eve_path, "r") as fp:
        for line in fp:
            eve_rule = json.loads(line)
            content.append(eve_rule)
            eve_type = eve_rule.get("event_type")
            if eventtype_only and eve_type in allowed_event_types:
                event_types[eve_type] += 1

    if not event_types:
        logger.error("No matching events found")
    if eventtype_only:
        filter_event_type(event_types=event_types)
        return
    filter_event_type_params(eve_rules=content)


def main():
    global output_path
    global eve_path
    args = vars(parser.parse_args())
    eve_path = args["path-to-eve"]
    output_path = args["output-path"]
    eventtype_only = args["eventtype_only"]
    init_logger()
    process_eve(eve_path=eve_path, eventtype_only=eventtype_only)


if __name__ == "__main__":
    main()
