import json

from eve2test import parser


def process_eve(path):
    with open(path, "r") as fp:
        content = json.load(fp)
    print(content.keys())


def main():
    eve_path, output_path = parser.parse_args()
    process_eve(path=eve_path)
    print("Success", eve_path, output_path)


if __name__ == "__main__":
    main()
