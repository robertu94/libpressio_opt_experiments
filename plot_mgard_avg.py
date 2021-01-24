#!/usr/bin/env python

import seaborn as sns
import pandas as pd
import argparse
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=argparse.FileType('r'))
    return parser.parse_args()


def prepare_data(args):
    df = pd.read_csv(args.input_file)
    df['Compression Time'] = df['time:compress_many'] / 1000.0
    df['filename'] = df['filename'].map( lambda x: str(Path(x).stem).replace('_','-'))
    df['tolerance'] = df['tolerance'].astype(float)
    return df

def setup():
    sns.set_style('whitegrid')
    sns.set(font_scale=2.0)
    matplotlib.rc('text', usetex=True)
    matplotlib.rc('ps', usedistiller='xpdf')


args = parse_args()
setup()
df = prepare_data(args)
g = sns.catplot(x="tolerance", y="Compression Time",  hue="filename", data=df, kind="bar")
ax: matplotlib.axes._subplots
for ax in g.axes[0]:
    ax.set_xticks(range(3))
    ax.set_xticklabels(["$10^{-5}$", "$10^{-4}$", "$10^{-3}$"])
    ax.set_yscale('symlog')
    ax.set_yticks(range(7))
    ax.set_yticklabels([str(i) for i in range(7)])

g.map(plt.axhline, y=0.0033, color="red", linewidth=4, label="libpressio+sz post-tuning")
g.map(plt.axhline, y=1.1000, color="green", linewidth=4, label="mgard-qoi post-tuning")
legend_data = g._legend_data
g.legend.remove()
g.add_legend(legend_data)
g.set_axis_labels(x_var="tolerance", y_var="seconds")

g.savefig("/tmp/mgard_avg.eps")
g.savefig("/tmp/mgard_avg.png")
