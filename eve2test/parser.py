import argparse


def parse_args():
    """
    Parse arguments and return them to main for processing.
    """
    parser = argparse.ArgumentParser(description="Convert eve.json to test.yaml")
    parser.add_argument("path-to-eve", metavar="<path-to-eve>",
            help="Path to eve.json")
    parser.add_argument("output-path", metavar="<output-path>",
            help="Path to the folder where generated test.yaml should be put")
    parser.add_argument("--eventtype-only", default=None, action="store_true",
            help="Create filter blocks based on event types only")

    # add arg to allow stdout only
    args = parser.parse_args()

    return args
