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

    args = parser.parse_args()

    eve_path = getattr(args, "path-to-eve")
    output_path = getattr(args, "output-path")
    return eve_path, output_path
