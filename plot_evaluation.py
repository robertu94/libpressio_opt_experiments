#!/usr/bin/env python

import argparse
import sys
import matplotlib
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("infile", type=argparse.FileType('r'), default=sys.stdin)
args = parser.parse_args()

sns.set_style('whitegrid')
sns.set(font_scale=1.5)
matplotlib.rc('text', usetex=True)
matplotlib.rc('ps', usedistiller='xpdf')

df = pd.read_csv(args.infile)

df.rename(columns={
    "sz:abs_error_bound": "Absolute Error Bound",
    "error_stat:psnr": "PSNR",
    "pearson:r": "Pearson's Coefficient",
    "size:compression_ratio": "Compression Ratio",
    "ks_test:p_value": "KS Test P Value",
    "composite:objective": "Objective",
    "spatial_error:percent": "Spatial Error \\% $(\\delta = 1e-4)$"
    }, inplace=True)
print(df.describe())

# x is the tick value; p is the position on the axes.


melted = df.melt("Absolute Error Bound")
melted.sort_values('Absolute Error Bound', inplace=True)
melted = melted[melted['variable'] != "Objective"]
plot = sns.relplot(data=melted, x="Absolute Error Bound", y="value", hue="variable", kind="line")
for ax in plot.axes[0]:
    ax.set_xscale('log')
    ax.set_yscale('symlog', linthresh=.05)
    ax.set_ylim(bottom=-0.05)

plt.axhline(y=.05, color=sns.color_palette()[1], linestyle='--') #ks test
plt.axhline(y=5, color=sns.color_palette()[2], linestyle='--') #spatial_error
plt.axhline(y=60, color=sns.color_palette()[3], linestyle='--') #psnr
plt.axhline(y=.99999, color=sns.color_palette()[4], linestyle='--') #pearson
plt.axvline(x=df[df['Objective'] == 0]['Absolute Error Bound'].min(), color='black', label="Objective")

plot.savefig("evaluation.eps")
