#!/usr/bin/env python

import argparse
import csv
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--infile", type=argparse.FileType('r'), default=sys.stdin)
parser.add_argument("--outfile", type=argparse.FileType('w'), default=sys.stdout)
args = parser.parse_args()

writer = None
last = {}
for line in args.infile:
    if line.startswith("==="):
        if not writer:
            writer = csv.DictWriter(args.outfile, fieldnames=list(last.keys()))
            writer.writeheader()
            writer.writerow(last)
        else:
            writer.writerow(last)
            last ={}
    else:
        parts = line.split('=')
        value = int(parts[-1])
        key = parts[0][:parts[0].index('<')]
        last[key] = value
