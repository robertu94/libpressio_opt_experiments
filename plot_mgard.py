#!/usr/bin/env python

import seaborn as sns
import pandas as pd
import matplotlib
from pathlib import Path
from matplotlib.ticker import FormatStrFormatter
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input", type=argparse.FileType('r'))
args = parser.parse_args()

def setup():
    sns.set_style('whitegrid')
    sns.set(font_scale=2.0)
    matplotlib.rc('text', usetex=True)
    matplotlib.rc('ps', usedistiller='xpdf')

def prepare_data(data):
    data['time:compress_many'] = data['time:compress_many']/1000.0
    #data['filename'] = data['filename'].map(lambda x: x.split('_')[-1].split('.')[0])
    data['filename'] = data['filename'].map( lambda x: str(Path(x).stem).replace('_','-'))
    data['compression ratio'] = data['size:compression_ratio']
    data['compression time'] = data['time:compress_many']
    data['psnr'] = data['error_stat:psnr']
    data = data[data['tolerance'] >=30]
    data = data[data['tolerance'] <=90]
    return data.sort_values("tolerance")

def compresion_time(data):
    g = sns.catplot(data=data, y="compression time", x="tolerance", hue="config", col="filename", kind="bar", sharey=True)
    for ax in g.axes[0]:
        ax.set_yscale('log')
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    g.set_ylabels('compression time (sec)')
    g.savefig("/tmp/opt-cloudtime.eps")
    g.savefig("/tmp/opt-cloudtime.png")

def compresion_ratio(data):
    g = sns.catplot(data=data, y="compression ratio", x="tolerance", hue="config", col="filename", kind="bar", sharey=True)
    for ax in g.axes[0]:
        ax.set_yscale('log')
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    g.savefig("/tmp/opt-cloudcr.eps")
    g.savefig("/tmp/opt-cloudcr.png")

def psnr(data):
    g = sns.catplot(data=data, y="psnr", x="tolerance", hue="config", col="filename", kind="bar", sharey=True)
    for ax in g.axes[0]:
        ax.set_yticks(list(range(30, 100, 10)))
    g.set_ylabels('PSNR (dB)')
    g.savefig("/tmp/opt-cloudpsnr.eps")
    g.savefig("/tmp/opt-cloudpsnr.png")



data = pd.read_csv(args.input)
data = prepare_data(data)
setup()
compresion_time(data)
compresion_ratio(data)
psnr(data)
