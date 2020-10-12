#!/usr/bin/env python

import argparse
import csv
import sys


def main(args):
    in_main = False
    last = {}
    writer = None
    for line in args.logfile:
        parts = line.split()
        if in_main:
            if line.startswith('-'):
                if writer is None:
                    if last:
                        fieldnames = set(last.keys())
                        writer = csv.DictWriter(args.outfile, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerow(last)
                else:
                    diffrows =  set(last.keys()) - fieldnames
                    for row in diffrows:
                        del last[row]
                    writer.writerow(last)
                last['filename'] = parts[1]
                last['tolerance'] = parts[-2].split('=')[1]
                last['config'] = parts[-1]
            else:
                try:
                    config = ":".join(parts[0].split(':')[-2:])
                    if config.split(':')[0] in ["sz", "mgard", "opt"]:
                        continue
                    param = float(parts[-1])
                    last[config] = param
                except ValueError:
                    pass

        if line.startswith("done preparing"):
            in_main = True

    diffrows =  set(last.keys()) - fieldnames
    for row in diffrows:
        del last[row]
    writer.writerow(last)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("logfile", type=argparse.FileType('r'))
    parser.add_argument("--outfile", type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()
    main(args)
