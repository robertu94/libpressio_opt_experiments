#!/usr/bin/env python

import argparse
import csv
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--outfile", type=argparse.FileType('w'), default=sys.stdout)
parser.add_argument("--infile", type=argparse.FileType('r'), default=sys.stdin)
args = parser.parse_args()


columns = ['sz:abs_error_bound', 'composite:objective', 'error_stat:psnr',
        'size:compression_ratio', 'ks_test:p_value', 'spatial_error:percent', 'pearson:r']

writer = csv.writer(args.outfile)
writer.writerow(columns)

INPUT_EXP = re.compile(r'input=\{([^}]+),\}')
OUTPUT_EXP = re.compile(r'output=\{([^}]+),\}')

for line in args.infile:
    row = []
    if line.startswith("final") or line.startswith("/"):
        continue
    in_exp = INPUT_EXP.search(line)
    if in_exp:
        row.extend(in_exp.group(1).split(','))
    out_exp = OUTPUT_EXP.search(line)
    if in_exp:
        row.extend(out_exp.group(1).split(','))
    writer.writerow(row)
