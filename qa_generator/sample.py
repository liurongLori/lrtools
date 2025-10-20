import argparse
import random


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument('-n', '--num', help="The samples' count", type=int, default=1000)
    parse.add_argument('-sn', '--sample_num', help="The samples' count of samples", type=int, default=50)
    parse.add_argument('-f', '--file', help="The urls file", required=True)
    args = parse.parse_args()
    with open(args.file) as f:
        data = [line.strip() for line in f.readlines()]
    sample = []
    for i in random.sample(list(range(len(data))), args.num):
        sample.append(data[i])
    sample_sample = []
    for i in random.sample(list(range(args.num)), args.sample_num):
        sample_sample.append(sample[i].split('\t')[0].strip())
    for item in sample:
        url = item.split('\t')[0].strip()
        print(item, url in sample_sample, sep='\t')
