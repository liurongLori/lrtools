import argparse
import re

if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument('-f', '--file', help="The urls file", required=True)
    args = parse.parse_args()
    pattern = re.compile(r"(\$\{[\w\.\s\'\"-]+\})")
    with open(args.file) as f:
        for line in f.readlines():
            for i in re.findall(pattern, line):
                print(i)